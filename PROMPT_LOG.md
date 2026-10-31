# Prompt log

Every prompt given to an AI tool today, copied as written.

## Claude Code (Claude Opus 5.5), desktop app

1. `hi`
2. `@"C:\Users\Mohit\Downloads\PSI hackathon case study assignment.pdf" @"C:\Users\Mohit\Downloads\Project_Drishti_Library.zip"`
   `understnd project completly and make everything i have a hackthon submission in 1 hr`
3. `Okay, so I want to get some details. Have you understand both the documents I gave you, and have you made the project that was specified to made you in the documentation according to you? Just check the entire project is working, every screen, every button is working, every feature is working. After that, I have to tell demo to the hackathon mentors. I need you to set up the demo step by step, and after setting up the demo, you also give me the script. I have to set in every demo and what the feature I have to showcase in every demo. And also one more thing, I need you to set up entire documentation of this project, so I can send it to my friend also, so it can understand what I built and what the project is end to end.`
4. `Okay, so I have attached the marking scheme on which we gonna be rated. Go through that and make sure I'll get rated best. And also I have given you the 8 important points that they send me. We also go through that and make sure it all must be followed and we are in a good place. And one more thing, if you can improve the UI, you can improve it. So it and make sure the documentation you have made also converted into PDF format. And one more thing, I need to send this project to my another teammate in repo form. So whatever data I am using should also be mentioned, because it can open that project in another Claude session, and everything must be streamlined. They don't have to make everything from scratch.`
   (with two screenshots: the marking scheme and the rules list)

## ChatGPT

<!-- ADD the prompts you gave ChatGPT today here, verbatim (your marking-scheme screenshot shows a ChatGPT window). -->

<!-- ADD any other prompts you gave to any AI tool today below, verbatim, before submitting. -->

## Prompts written for the engine's agents

These are the instructions the engine gives its own agents (full text in `engine/prompts/`):

- `00_shared_rules.md`: citation, no-invention, source-priority and credit-sharing rules for every agent
- `02_rules.md`: Rules agent (contract first, approvers, banned terms)
- `03_results_spec.md`: Results-spec agent (signed definitions, same-instrument comparisons, split windows at other causes)
- `05_exposure.md`: Exposure judge (direct, combination, media, vendor-side claims)
- `06_timeline.md`: Timeline / story spine agent
- `06_results_sheet.md`: Results sheet agent
- `06_writer.md`: Writer agent (three readers + champion)
- `06_approval.md`: Approval request agent
- `07_fix.md`: Fixer agent (gets the verifier's refused lines back in live mode)
