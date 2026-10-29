// Re-embeds questions.json and analyticsexam_vi.json into ../sas_exam_simulator.html so it works when opened from disk (file://).
// The harvester only rewrites the embeddedQuestionBank block, so the Vietnamese AnalyticsExam explanations survive new harvests.
// Usage: node question_bank/build_practice_test.js
const fs = require('fs'), path = require('path');
const dir = __dirname;
const read = f => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
const bank = read('questions.json');
const embed = (file, id, data, label) => {
  const json = JSON.stringify(data).replace(/</g, '\\u003c'); // keep "</script>" out of the embedded block
  const re = new RegExp(`(<script id="${id}" type="application/json">)[\\s\\S]*?(</script>)`);
  const html = fs.readFileSync(file, 'utf8');
  if (!re.test(html)) throw new Error(`no ${id} block in ${file}`);
  fs.writeFileSync(file, html.replace(re, (m, a, b) => a + '\n' + json + '\n' + b));
  console.log(`Embedded ${label} into ${path.basename(file)}`);
};
const sim = path.join(dir, '..', 'sas_exam_simulator.html');
embed(sim, 'practiceBank', bank, `${bank.questions.length} questions`);
const vi = read('analyticsexam_vi.json');
embed(sim, 'aeVietnamese', vi, `${Object.keys(vi).length} Vietnamese AnalyticsExam explanations`);
