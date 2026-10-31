# 1. Project story spine (internal, every line cited)

## Timeline

| Date | What happened | Who decided | Why it matters | Source |
| --- | --- | --- | --- | --- |
| 28 Jan 2026 | Client's Head EHS writes in after a LinkedIn post: about 146 CCTV cameras, serious incidents, manual audits "not giving us the true picture" | Client Head EHS | The client's problem in their own words | [D15:L5-13] |
| 6 Feb 2026 | Discovery call: four LTIs last year; walk compliance "seventy-something" against a corporate target of ninety; walks announced in advance | Client Head EHS | The "before" | [D03:L10] [C:lti_2025] [D03:L14] [D03:L22] |
| 6 Feb 2026 | TURNING POINT: vendor warns the first camera number will look worse than the walk score; client thanks them for it | Vendor architect | Trust built on an uncomfortable truth | [D03:L24] [D03:L66] |
| 6 Feb 2026 | Unit Head adds two asks: face-recognition attendance and truck queues at the gate | Unit Head | Later both become scope changes | [D03:L42] [D03:L46] |
| 6 Feb 2026 | IT/OT security sets the non-negotiables: no cloud, no internet from OT, jump host only, no footage leaves the plant | Client IT/OT head | Gatekeeper constraint for the whole project | [D03:L56] |
| 14 Feb 2026 | RFQ issued: helmet, vest, restricted zones mandatory; on-prem mandatory; face attendance and harness optional | Procurement | What was asked for | [D04:L17] [D04:L23-25] |
| 17 Feb-2 Mar 2026 | Security review: 3 blockers (registry pull, VPN, snapshots on WhatsApp) all resolved; text-only alerts chosen | Client IT/OT head | Gatekeeper proof | [D16:L13-15] [D16:L31-33] [D16:L45] |
| 24 Feb 2026 | Proposal: PoC 12 cameras, pilot 40, plant-wide 146; targets 95% PPE, -70% zone entries, 2 min response, 5% false alarms; harness not offered | Vendor | What was promised | [D05:L25-28] [D05:L37-40] |
| 5 Mar 2026 | BRD v2 signed: targets lowered to 90% / -50% / 3 min / 10%; baseline switched from manual walks to camera-measured pilot weeks 1-2 | Client EHS review | Targets renegotiated before work began | [D06:L14] [D06:L40-48] |
| 9 Mar 2026 | PoC purchase order (12 cameras, 6 weeks) | Head EHS within delegation | Start of paid work | [D08:L12] [D08:L16] |
| 19 Mar-24 Apr 2026 | PoC runs; 2 low-resolution cameras swapped; false alarms 23% (dust, reflective sacks) | Vendor ML lead | First failure, honestly reported | [D11:L7] [D11:L9] [D12:L19] |
| 31 Mar 2026 | Business owner and first champion (Head EHS) leaves the company; successor starts 7 Apr | Client | Champion lost mid-project | [D17:L11] [D17:L13] |
| 17 Apr 2026 | TURNING POINT: PoC review. New Head EHS rejects 23% false alarms, demands <10% checked by her team; shift in-charge says snapshots ended arguments with contractors ("Not punishment, proof"); pilot approved with kiln added | New Head EHS, Unit Head | The project nearly died and was rescued by evidence | [D12:L17-29] [D12:L39] [D12:L47-49] |
| 22-28 Apr 2026 | CR-01: kiln platform hot-zone (face shield) replaces "area to be confirmed" | Head EHS, Unit Head | Scope change driven by a February burn injury | [D07:L7-10] |
| 4 May 2026 | Pilot PO: 40 cameras, kiln rule, optional face attendance | Unit Head | Deal grows | [D08:L22-24] |
| 11 May 2026 | Pilot go-live, 40 cameras | Vendor | Measurement window starts | [D11:L13] [D30:L27] |
| 14-20 May 2026 | TURNING POINT: Corporate Legal stops face recognition (DPDP Act consent); decision not to proceed in 2026 | Corporate Legal | Scope removed for privacy | [D18:L11-17] [D18:L40-41] |
| 2 Jun 2026 | Face module removed from the build (not just disabled); client verified package hash; PO amended with credit | Vendor ML lead, client IT | Gatekeeper proof | [D18:L53-54] [D30:L21] [D08:L29-31] |
| 9-11 Jun 2026 | INC-0611: client contractor firmware update kills 22 streams for about 41 hours; software showed "connected" | Shared fault | Incident handled openly | [D09:L9-17] [D09:L33] |
| 15 Jun 2026 | Retrain on 4,200 site frames on premises (v1.3); false alarms fall | Vendor ML lead | The fix for the PoC failure | [D30:L16-17] [D13:L20] |
| 26 Jun 2026 | Steering committee: Head EHS credits safety week, toolbox talks and gang suspensions too; Finance rejects vendor's benchmark ROI; plant-wide approved on Finance's numbers | Unit Head, Finance | Credit shared; money claims disciplined | [D13:L22-26] [D13:L36] [D13:L48] |
| 1 Jul 2026 | Vendor email claims 74% to 96.6%; Head EHS rejects it (wrong baseline, best zone and week); BRD definitions used from then on | Head EHS | The engine treats this as a "refuse" example | [D19:L13-17] [D19:L36-40] [D19:L57] |
| 6 Jul 2026 | Pilot accepted with conditions: K1 and K4 met, K2 and K3 missed; client to install tail-pulley guards, control room to phone after 5 min | Head EHS, Unit Head | Missed targets on record | [D10:L11-22] |
| 9-14 Jul 2026 | Plant-wide order plus CR-03 gate analytics (number-plate cameras, weighbridge feed) | Unit Head, corporate capex | Path to scale | [D07:L22-26] [D08:L37-38] |
| 3 Aug 2026 | Gate analytics live; release v2.0 plant-wide | Vendor | K5 measurement starts | [D11:L24] [D30:L5-8] |
| 4-12 Aug 2026 | Control-room phone escalation enabled; client finishes tail-pulley guards; pre-zone warning added | Client + vendor | Remediation of K2/K3 | [D11:L26-27] [D33:L9-10] |
| 18 Aug 2026 | Client commissions a second weighbridge (separate client capex) | Client | Other cause of gate result | [D26:L80] [D14:L22] |
| 25 Aug 2026 | Logistics starts dispatch slots using the queue alerts | Client logistics | Main cause of gate result, enabled by the system | [D26:L87] [D33:L7] |
| 31 Aug 2026 | All 146 cameras live, 3 days after plan (batch 1 had slipped 1 week on a client-side PoE switch failure) | Vendor | Delivered scope | [D11:L22] [D11:L28] |
| 3 Sep 2026 | Two invoices paid late because GRN was pending on client side | Procurement | Process lesson | [D20:L3-39] |
| 9-10 Sep 2026 | Corporate pre-assessment: provisionally B+ (last year C); assessor cites "continuous monitoring with evidence-based closure" | Corporate audit | Outcome the sponsor cares about (provisional) | [D14:L32] |
| 18 Sep 2026 | QBR: all-camera PPE dip explained by new cameras; K2 and K3 conditions now met; gate attribution split agreed with Finance | Unit Head, Finance | Honest results | [D14:L8-30] |
| 18 Sep 2026 | Unit Head agrees to an anonymised case study only via Legal and Corporate Comms; no plant name, state, capacity, photos | Unit Head | Rules for this case study | [D14:L40] [D14:L44] |
| 20-29 Sep 2026 | Vendor award nomination named the client without approval; withdrawn after Legal's email | Vendor | Exposure the engine must prevent | [D42:L26-27] |
| 24-28 Sep 2026 | Vendor asks for WhatsApp approval of a "74% to 97%, zero LTIs" headline; refused; Legal sets the MSA clause 15 process | Unit Head, Legal | Why the engine has a human gate | [D22:L10-13] [D22:L28-29] [D22:L43-49] |
| 28 Sep 2026 | Head EHS (champion) privately advises waiting for the final audit on 27 Oct, when a named version may be possible | Head EHS | Timing of the approval request | [D22:L60-62] |
| 30 Sep 2026 | Head EHS posts publicly about the programme and names the vendor | Head EHS | Public link between client and vendor already exists | [D35:L3-12] |

## What was really sold vs delivered

| Promised (proposal) | Signed (BRD v2) | Delivered | Changed, why | Source |
| --- | --- | --- | --- | --- |
| PPE compliance 95% | 90% on camera, last 4 pilot weeks | 91.1%, met | Target lowered by client EHS before work began | [D05:L37] [D06:L14] [C:k1_final] |
| Zone entries -70% | -50% | -46% in pilot (missed); -77% by Sep after client guards and pre-zone | Target lowered; remediated with client action | [D05:L38] [D06:L14] [C:k2_change] [C:k2_change_sep] |
| Response under 2 min | 3 min | 4.9 min in pilot (missed); about 2.1 min by Sep after phone escalation | Process fix by control room | [D05:L39] [D10:L13] [C:k3_sep] |
| False alarms under 5% | under 10% | 9.7% (met); about 6.2% plant-wide in Sep | Retrain on site images | [D05:L40] [C:k4_final] [C:k4_sep] |
| Face attendance (option) | Optional pending Legal | Removed from build | Privacy law; Legal decision | [D05:L27] [D07:L14-18] |
| Harness detection | Not offered | Not delivered | Camera angles | [D05:L31] |
| Not in proposal | Not in BRD | Kiln face-shield rule | Burn injury in February | [D07:L7-10] |
| Not in proposal | Not in BRD | Gate turnaround analytics, K5 | Unit Head's detention cost | [D07:L22-26] |
