# 2. Results sheet (internal; full working in 02b_calc_ledger.md)

Method: every ratio is a ratio of sums over the window (not an average of weekly percentages), recomputed from the raw ViewOS export, and matches the signed acceptance certificate. [D24:L5-20] [D10:L3-14]
Counting rule: a "person observed" is one tracked person per camera per 10-minute window; the same person on two cameras counts twice, so compliance is a rate of observations, not of individuals. [D34:L19-20]

## Safety results (pilot: 40 cameras, 11 May-3 Jul 2026)

| KPI | Definition | Baseline (window) | Result (window) | Target | Status | What else contributed | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| K1 PPE compliance | helmet AND vest / persons observed, pilot cameras | 68.9% (pilot weeks 1-2) | 91.1% (last 4 pilot weeks) | 90% | Met, +22.2 pts | Plant safety week, daily toolbox talks, 2 contractor gangs suspended | [D06:L45] [C:k1_base] [C:k1_final] [C:k1_gain_pts] [D13:L22] |
| K2 Restricted-zone breaches | per 1,000 camera-hours | 5.58 | 3.00 | -50% | Not met, -46% | People stepping over to clear spillage | [C:k2_base] [C:k2_final] [C:k2_change] [D13:L12] |
| K3 Alert acknowledgement | median minutes, alert to ack | 9.3 min in week 1 | 4.9 min last 4 weeks; 3.5 min final week | 3.0 min | Not met | Week of 8 Jun hit by 41-hour outage | [C:k3_week1] [C:k3_final_alertw] [C:k3_last_week] [D10:L13] [D10:L24] |
| K4 False alarms | share marked false in EHS daily sample | 20.1% before retrain | 9.7% last 2 pilot weeks | under 10% | Met | Checked by client EHS, not vendor | [C:k4_prefix] [C:k4_final] [D12:L25] |

## After remediation and scale (to 27 Sep 2026)

| Result | Value | Window | What else contributed | Source |
| --- | --- | --- | --- | --- |
| PPE, 40 pilot cameras | 94.4% | 31 Aug-27 Sep | Gang bonus for teams above 95% approved by EHS | [C:k1_pilot_sep] [D36:L26-27] |
| PPE, 106 new cameras | 72.0% in first week, 87.2% now | 6 Jul vs 31 Aug-27 Sep | Gate yard: transporter drivers without helmets | [C:k1_scale_first] [C:k1_scale_sep] [D14:L14] |
| PPE, all cameras | 89.2% | 31 Aug-27 Sep | Mix of mature and new areas; explains the dip on the dashboard | [C:k1_all_sep] [D14:L12] |
| Zone breaches, pilot cameras | 1.26 per 1,000 h, -77% vs baseline | 31 Aug-27 Sep | Client installed physical tail-pulley guards (12 Aug); vendor pre-zone warning | [C:k2_sep] [C:k2_change_sep] [D11:L27] |
| Acknowledgement | about 2.1 min | 31 Aug-27 Sep | Control room phones the in-charge after 5 minutes (client process) | [C:k3_sep] [D11:L26] |
| False alarms, all cameras | 6.2% | 31 Aug-27 Sep | Retrain on 4,200 site frames | [C:k4_sep] [D30:L16] |
| Supervisor survey | alerts useful 4.2 / 5; noise 1.9 / 5; 15 of 18 would recommend | 14-16 Sep | Comments of S15-S18 repeat S01-S04 word for word: possible transcription error, so comments are not quoted | [C:survey_useful] [C:survey_noise] [C:survey_recommend] [D28:L2-19] |

## Gate (K5, added by CR-03)

| Step | Avg turnaround | Window | Source |
| --- | --- | --- | --- |
| Manual register baseline | 93.5 min | Jun-Jul, 55 days with data; handwritten, rounded to 5 min, 6 pages missing | [C:tat_manual] [D24:L30-31] |
| Number-plate cameras, before weighbridge 2 | 88.4 min | 3-16 Aug | [C:tat_v_first] |
| After weighbridge 2 (client capex), before slots | 82.8 min | 18-24 Aug | [C:tat_v_wb] |
| After dispatch slots run from the queue view | 67.6 min | 25 Aug-30 Sep | [C:tat_v_slots] |

- K5 result: -28% against the signed manual baseline (target -15%, met), but the baseline instrument is weak, so the case study uses -24% on the same instrument. [C:tat_k5_vs_manual] [C:tat_k5_vs_anpr] [D07:L26]
- Attribution: about 5.6 minutes fell in the weighbridge-2 week and about 15.2 minutes after dispatch slots, matching the vendor architect's own split. [C:tat_wb_effect] [C:tat_slot_effect] [D14:L28]
- The slot system is a client logistics decision that the queue view made possible; credit is shared. [D14:L28] [D21:L16-18]

## Money (only what the client's Finance measured)

| Item | Value | Status | Source |
| --- | --- | --- | --- |
| Detention paid, Jun-Jul average | 12.1 lakh/month | Measured in SAP by client Finance | [C:det_base] [D21:L14-15] |
| Detention, September | 3.9 lakh/month | ASSUMED: Finance estimate to month end | [C:det_sep] [D21:L14] |
| Reduction | 8.2 lakh/month; 98 lakh/year only if it holds | ASSUMED annualisation; one month is not a trend | [C:det_saving_m] [C:det_saving_y] [D21:L18] |
| Project share of the gate saving | not stated as a number | Finance asks to credit "a share" until Oct-Dec data | [D21:L16-18] |
| Insurance | 7-12 lakh/year possible from January | Not realised; depends on final audit | [D21:L21] |
| Avoided LTIs | not monetised | Finance: should not be claimed | [D21:L24] |
| Project cost | 107.7 lakh + AMC 12 lakh/year | Measured | [C:total_cost] [D21:L28-29] |
| Payback, half of gate saving credited | 26 months (Finance's simple view), 35 months if AMC is netted | ASSUMED | [C:payback_half_noamc] [C:payback_half] [D21:L31] |

## Where sources disagree

| Claim | Sources | We use | Why | Source |
| --- | --- | --- | --- | --- |
| PPE baseline | 73.8% manual walks vs 68.9% camera weeks 1-2 vs 61% PoC | 68.9% | BRD v2 signed baseline; walks are announced and not comparable | [C:walk_q4] [C:k1_base] [D12:L11] [D06:L40-41] |
| PPE result | 96.6% (vendor email) vs 91.1% (certificate) | 91.1% | 96.6% is the packing zone in its best week only | [C:packing_best] [D19:L36] [C:k1_final] |
| Response-time baseline | "9+" (vendor email) vs 9.3 min week 1 | 9.3 min, week 1 only | No baseline in BRD for K3; week 1 is a start point, not a baseline | [D19:L15] [C:k3_week1] [D06:L47] |
| Outage length | 41 hours (incident report) vs "fifteen hours" (steering committee) | 41 hours of stream loss | The fifteen hours is the detection delay, not the outage | [D09:L9] [D13:L18] |
| Gate baseline | 93-94 min manual vs 88 min first ANPR weeks | both shown; 88 used outward | Same-instrument comparison is defensible | [D14:L24] [C:tat_v_first] |
| Release v1.4 date | 24 Jun (tracker) vs 20 Jul (changelog) | 20 Jul release, code merged 24 Jun | Tracker marks code done; changelog marks deploy | [D11:L19] [D30:L10] |

## Numbers we refuse to use

| Claim | Where it appears | Why refused | Source |
| --- | --- | --- | --- |
| "74% to 97%" / "+31%" | vendor email, sales deck, headline draft | Mixes manual baseline with best zone-week; client rejected it in writing | [D19:L13] [D41:L3-17] [D19:L36] |
| "Zero LTIs since go-live" as a result | vendor email, sales deck | Seven months at a base rate of about one LTI a quarter proves nothing; client's own Head EHS refuses to claim it | [D19:L39-40] [D14:L36] |
| "Rs 2.3 Cr annual savings" | sales deck | Includes 88 lakh avoided LTIs and 30 lakh benchmark productivity, both rejected by Finance | [D41:L3-17] [D13:L36] [D21:L24] |
| "Alert response 9 min to 2 min" as the system's result | sales deck | The 2-minute level arrived after the client's phone-escalation rule | [D41:L3-17] [D11:L26] |
| Near-miss reports rising | EHS register | From 15 Jun system alerts can be logged as near-misses, so the series changed definition | [D25:L19] |
