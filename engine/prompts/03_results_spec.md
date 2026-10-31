# Agent 3: Results spec

Find every result the project was judged on: the signed requirements (KPI definitions, baselines, windows, targets),
change requests that added KPIs, acceptance documents, and the client finance team's value notes. Then read the data
dictionary and raw exports.

Output JSON `{"calcs": [...]}` for the calculator. Each calc: id, label, op (ratio_of_sums | mean | median |
weighted_mean | sum | count | pct_change | diff | formula), file, where (filters on columns), columns, unit, round,
assumed (true if it projects or attributes rather than measures), note (why this definition, which source it follows).

Rules:
- Use the client's signed definition and window, not the most flattering one. Add the flattering ones that the vendor
  sales team used as separate calcs labelled "NOT a KPI", so the results sheet can show why they are rejected.
- Ratios are ratio of sums over the window, not averages of weekly percentages.
- When the instrument changed (e.g. manual register -> sensor), add a same-instrument comparison as well.
- When something else happened in the window (new equipment, process change, client action), add calcs that split the
  window at that date so the results sheet can show "what else contributed".
- Money only where the client measured it. Projections are `assumed: true`.
