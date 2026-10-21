# Skills Network grading feedback — first attempt

Source: https://mark.skills.network/learner/2432/successPage/1871008

Actual assessment: **10/16 (63%), Failed**; passing grade 75%.
This assessment is separate from the original local verification checklist.

Passed questions: 1, 2, 4, 6, 8, 12, 13, 14, 15, 16.
Failed questions: 3, 5, 7, 9, 10, 11.

## Remember for resubmission

- Questions 1 and 6 take public GitHub file URLs.
- Questions 2, 4, 8, 10, 12, 13, 15 take pasted source code with indentation.
- Questions 3, 5, 7, 9, 16 take pasted terminal text, NOT screenshot uploads.
- Only questions 11 and 14 require image uploads.
- Do not submit timeouts, all-None dictionaries or failed tests as successful evidence.
- Do not fabricate output, paths, numeric predictions, passing tests or screenshots.

## Exact corrections from the report

Question 3 requires a real Python interactive session using `python3`,
`from emotion_detection import emotion_detector`, and
`print(emotion_detector('I am really mad about this'))`, then `exit()` and
`python3 test_emotion_detection.py`. The prompt explicitly requires the genuine
`/home/project/final_project` path. The prior Windows command, other sample
sentence and failed response do not meet this requirement. Use the actual
Skills Network lab when producing this evidence; never relabel a Windows run.

Question 5 needs printed numeric scores for all five emotions and an actual
dominant emotion. Six None values do not qualify.

Question 7 requires the entire real output of:

```sh
python3 -c "from EmotionDetection.emotion_detection import emotion_detector; print(emotion_detector('I am very angry'))"
```

It must show the exact module import, five emotion scores and
`'dominant_emotion': 'anger'`.

Question 9 needs all five required live tests passing with `OK`.
Ten passing local mock/contract tests cannot replace them.

Question 10 was rejected specifically because the reference requires
`from EmotionDetection.emotion_detection import emotion_detector` and
`app.run(host="0.0.0.0", port=5000)`. Both lines are now corrected in server.py.
This correction has not yet been graded in a new attempt.

Question 11 needs `6b_deployment_test.png` showing valid input AND the formatted
prediction. The first image showed an error and was correctly rejected.

Questions 13, 15 and 16 already earned 1/1. The report also displays a second,
zero-point failure-alternative criterion as unmet. That is not an additional
lost point. Do not treat it as a reason to change accepted functionality.

The Watson endpoint remains an external blocker in the recorded Windows run.
Changing answer formatting alone cannot produce the missing live evidence.
