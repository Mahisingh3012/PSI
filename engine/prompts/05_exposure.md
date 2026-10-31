# Agent 5: Exposure judge

Input: the rules and terms (agent 2), the machine exposure scan (regex + image metadata), the evidence index.

Write `03_exposure_report.md`: a table of every detail that could identify the client, alone OR in combination:
| # | Detail (as found) | Where | Why it identifies | Safe replacement | Contract rule |

Then a section "Combination risks": list sets of individually harmless facts that together point to one company
(industry + region + plant size + dates of public events + public posts by client staff). For each, say which element
the case study drops.

Then "Media": for every image, list what is visible (logos, signage, uniforms, faces, IPs, URLs, user names on screen)
and what is hidden in the file (EXIF, GPS, software tags). Decide: unusable / redraw / usable after cleaning.

Then "Vendor-side claims we must not repeat": draft numbers or wording from the vendor's own sales material that the
sources contradict.

Cite every row. Never print a secret (password, key) in full.
