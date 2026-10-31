# 4. Case study: anonymised version (traced copy; the clean copy strips the tags)

## What happens on a cement plant floor when nobody announces the safety walk

An Indian cement manufacturer used its existing security cameras to see real PPE compliance all day, not just on announced walks. 
On 40 pilot cameras, compliance measured by the cameras rose from 69% to 91% in eight weeks, and those areas held 94% three months later. 
The plant's own teams did the hard work: a safety week, daily toolbox talks and firm action with contractor gangs; the system made every violation visible with evidence. 
Everything runs inside the plant network: no cloud, no internet from the edge servers, and no footage leaves site. 

## For the gatekeeper: one-page fact sheet

| Question | Answer | Source |
| --- | --- | --- |
| Where does processing run? | On vendor-supplied edge GPU servers inside the client's OT network | |
| Internet access? | None from the edge servers; model updates arrive as signed packages that the client's IT team installs | |
| Vendor remote access? | Only through the client's jump host, session recorded, approved per session | |
| Do images reach phones? | No; phone alerts carry text only, the snapshot opens on the console inside the plant network | |
| Does it identify people? | No; it detects persons and PPE, with no identification of individuals and no face templates stored | |
| A face-recognition attendance option was ordered; what happened? | The client's Legal team stopped it under the Digital Personal Data Protection Act; the vendor removed the module and its model files from the build, not just switched it off, and the client's IT verified the installed package hash | |
| Retraining on site images? | Done on a training box on premises; images never left site | |
| Security review | The client's IT/OT security head raised 3 blockers before the pilot; all resolved before clearance | |
| Certifications | Vendor SOC 2 and ISO 27001; on-prem deployment checklist mapped to ISO 27001 Annex A | |
| Incidents | A contractor firmware update silently cut 22 camera streams for about 41 hours; the vendor added a frame-arrival health alarm (5 minutes) and a joint change-control rule; no safety incident occurred in the gap | |

## For the user: a normal day, before and after

Before: two announced safety walks a day, and shift teams were warned on their group chat that a walk was coming. 
The cameras recorded, but nobody watched the conveyor or kiln screens. 
The first camera week was humbling: the measured number was lower than the walk score, as the vendor had warned on the first call. 
The first weeks were noisy: in the proof of concept, 23% of alerts were false, mostly reflective strips on sack pallets read as vests and dust hiding helmets. 
The new Head of EHS set the bar: under 10% false alarms, checked every week by her own team, and alerts going straight to the area in-charge. 
After a retrain on 4,200 site images, false alarms fell from about 20% to under 10% on the client's own sample, and to about 6% plant-wide by September. 
On the floor, the alert snapshot ended arguments: a shift in-charge showed a contractor gang leader the photo, and the argument stopped. 
Within weeks, gang leaders in packing were checking helmets themselves before the shift started. 
When alerts piled up at shift change near the lockers, the team excluded that corridor for those minutes and logged it as an open rule change, not a hidden exception. 
Response got faster when the control room began phoning the in-charge if an alert was not acknowledged in 5 minutes. 
Supervisors rated the alerts 4.2 out of 5 for usefulness and 1.9 out of 5 for noise; 15 of 18 would recommend it to another plant. 
Not everything is solved: night shifts lag, and the truck yard, where most people are transporters' drivers, is the weakest area. 

## For the buyer: what it was worth

Headline: real PPE compliance on camera rose from 69% to 91% in an eight-week pilot and reached 94% in those areas three months later. 
Restricted-zone entries on the pilot cameras fell 46% during the pilot (target was 50%) and 77% after the plant added physical guards and the system added a pre-zone warning. 
Truck turnaround at the gate fell 24%, from about 88 to about 68 minutes, measured on the same number-plate cameras throughout. 
About 6 minutes of that came with a second weighbridge the client installed, and about 15 minutes after the logistics team started dispatch slots based on the live queue view. 
The client's finance team measured transporter detention charges falling by about two thirds in September (ASSUMED: September is Finance's month-end estimate), and chose to credit the system with a share until a longer trend is in. 
The finance team's simple payback, crediting half of the gate saving and nothing else, is a little over two years; this is ASSUMED, not measured. 
Safety savings were deliberately not monetised: a few injury-free months are too short to prove anything. 
Path to scale: from 12 cameras to 40 to every existing camera in the plant in about six months, with new areas starting at 72% compliance and climbing to 87% by September. 

## What we got wrong, and fixed

- False alarms were 23% in the proof of concept; we fixed them with a retrain on site images before scaling. 
- We missed two of four pilot targets (zone entries and response time); the pilot was accepted with conditions, and both were met by September with actions on both sides. 
- Our software showed cameras as "connected" while no frames arrived for about 41 hours; we now alarm on missing frames within 5 minutes. 
- An early results summary from our own team mixed baselines; the client corrected it, and we now report only on the signed definitions. 

## For the champion: a note to forward

The cameras we already owned now show safety as it is all day, not on announced walks. 
Compliance on camera went from 69% to 91% in the pilot and has held at 94% where it started. 
False alarms are under 10%, checked every week by our own EHS team, so the floor trusts the alerts. 
No video leaves the plant, no faces are recognised, and our IT and Legal teams verified both. 
Gate turnaround is down about a quarter, with our own logistics and weighbridge changes doing part of the work. 
