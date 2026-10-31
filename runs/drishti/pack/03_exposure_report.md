# 3. Exposure report (internal)

Machine pass: regex and image-metadata scan in exposure_scan.md; this report is the judged version. Rules R1-R12 are in the rules file written by the Rules agent. [NO-CLAIM]

## Direct identifiers

| # | Detail | Where | Why it identifies | Safe replacement | Contract rule | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Client legal and short name | contract, PO, certificate, repo | Names the client | "an Indian cement manufacturer" | MSA 15.1, 15.2(a) | [D02:L5] [D02:L24-28] |
| 2 | Unit name and state | emails, BRD, repo, public profile | Location below country | "a cement plant in India" | MSA 15.2(b) | [D15:L19] [D02:L29] |
| 3 | Sister unit name (new Head EHS came from it; its team visited) | PoC review, WhatsApp, handover | Second site name | "a sister plant" or removed | MSA 15.2(b), 15.2(c) | [D12:L9] [D36:L25] |
| 4 | Clinker capacity of the line | discovery call, site config | Capacity is banned and is in the annual report | removed | MSA 15.2(c) | [D03:L50] [D31:L6] [D40:L8] |
| 5 | Headcount (employees, contract workforce), number of plants (integrated units) | public profile | Headcount banned | removed | MSA 15.2(c) | [D40:L8-9] |
| 6 | Client-side people (Unit Head, Head EHS, ex-Head EHS, IT/OT head, Finance, Legal, Comms, Procurement, shift staff, gang leaders, EHS officers) | everywhere | Real names of client staff | role titles only, no quotes attributed by name | MSA 15.1, 14.1 | [D06:L25-29] [D36:L4-27] |
| 7 | Project name chosen by the client | BRD, repo, public post | The client's Head EHS used it in a public post that also names the vendor | "the safety-vision programme" | MSA 15.1 | [D06:L7] [D35:L7] |
| 8 | Sender emails, domains and the mobile number in the Head EHS signature block | email threads | Contact data | removed | MSA 14.1 | [D15:L3-20] |
| 9 | PO numbers, contract no., capex no., GSTIN, vendor code, invoice numbers | PO file, invoices, emails | Unique documents | removed; deal size as a band only | MSA 14.1 (commercial terms) | [D08:L5-6] [D08:L42] [D27:L1-6] |
| 10 | Exact PO values and payment terms | PO file | Commercial terms | "a programme in the low single-digit crore band" (only if client approves) | MSA 14.1 | [D08:L12] [D08:L37-40] |
| 11 | Repository name, branch, IPs, console URL, RTSP URLs, NVR names | repo README and config | Internal systems; RTSP URLs carry a credential variable | never shown; redrawn generic diagram | MSA 14.1 | [D34:L5-14] [D31:L8-21] |
| 12 | Camera IDs and area names (packer numbers) | WhatsApp, config, snapshot | Plant layout | removed | MSA 14.1 (plant layouts) | [D36:L4] [D31:L16-18] |
| 13 | CCTV brands of the existing cameras | discovery call, RFQ | Identity of suppliers | "mixed-brand existing CCTV" | MSA 14.1 | [D03:L18] |
| 14 | Exact detention amounts in lakh, insurance premium, cost per LTI | Finance email, steering committee | Client financials | percentages and ranges only | MSA 14.1 | [D21:L14-15] [D13:L36-40] |
| 15 | Safety incidents with dates and body parts (fall, burn, crush) | EHS register, call transcript | Safety incident records | "four lost-time injuries the year before" only | MSA 14.1 | [D25:L4-15] |
| 16 | Audit ratings (C, provisional B+) | QBR, discovery call | Internal group audit; provisional | named version only, after final audit | MSA 14.1 | [D14:L32] [D03:L30] |

## Combination risks

| Combination | Why together it names the client | What we drop | Source |
| --- | --- | --- | --- |
| Indian cement + plant-wide count of 146 cameras + second weighbridge commissioned in August + truck-parking press release | The weighbridge press release is public and dated; a reader can match it to our gate story | No weighbridge capex amount, no dates for it outward; say "a second weighbridge" only | [D40:L15] [D26:L80] [D11:L28] |
| Head EHS's public post (names the vendor, the programme, "10 points below" the walk score, packing shifts) + our story of "camera number lower than walk score" | The post is public, so any case study by this vendor with the same arc points to her company | No programme name, no "10 points below" phrase, no packing shift names, none of her post's wording; we tell the arc in our own words and figures rounded from our ledger | [D35:L3-12] |
| "Leading cement major" + headline numbers | Client's Unit Head said anyone in the industry would know | "an Indian cement manufacturer" only | [D22:L29] |
| Competitor plant forty km away + region + group audit in October | Region plus timing narrows to a few companies | No region, no audit month outward | [D14:L40] [D03:L30] |
| Award nomination that named the client (withdrawn) | Award shortlists are public | Never re-submit without approval | [D42:L26-27] |

## Media

| File | Visible | Hidden in file | Decision | Source |
| --- | --- | --- | --- | --- |
| Alert snapshot from a packing camera | Company and unit name on signboard, helmet logo, uniforms, camera ID, internal IP, timestamp | EXIF: camera make/model, description naming the unit, GPS coordinates of the plant | UNUSABLE (MSA 15.2(d), 14.3); replaced by a labelled illustration | [D02:L31] [D02:L17-18] |
| Dashboard export, weekly PPE | Client and unit name in title, console IP and a vendor user's email in footer, all-camera line that dips without explanation | Software tag only | REDRAWN from the ledger with cohorts split | [D14:L8-12] |
| Architecture as built rev C | Client and unit name, IP ranges, camera count, CCTV brands, author name | none | REDRAWN generically | [D34:L5-14] |

## Vendor-side claims we must not repeat

- The sales deck asks to use the alert snapshot ("looks great") and add the client's logo; both are banned by MSA 15.2(d) and 15.1. [D41:L3-17] [D02:L24-31]
- The sales deck and the WhatsApp-approval email use a mixed baseline (74%) and a cherry-picked result (97%); see the results sheet. [D41:L3-17] [D22:L11]
- The Head EHS asked that her remark about her previous plant's alarms is never used. [D22:L62]
