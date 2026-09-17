# The Booking Ledger — expanded analysis

A local revision of the hotel-booking dashboard. No live deployment has been performed.

## What is new

- Cancellation volume by market segment: Online TA accounts for approximately 20,727 cancellations compared with Groups' 12,105, despite Groups' higher cancellation rate.
- Lead-time-adjusted property comparison: holding four booking-window shares constant produces approximately 40.70% for City Hotel and 29.46% for Resort Hotel, an 11.24-percentage-point gap.
- Calendar normalization: under the page's stated July 2015–August 2017 coverage, July and August each occur three times, other months twice. May has the highest combined count per month occurrence after this limited adjustment.
- Coverage audit: monthly counts sum to 75,166, compared with 119,389 headline records. The segment and channel views also omit records.
- Published channel revenue divided by listed bookings, explicitly distinguished from profit and ADR.
- A break-even calculator with user-specified treatment effect, incremental value and cost.
- A management conclusion and proposed prospective intervention test.

## Source and boundaries

The input is the DATA object in https://takizawadaiki.github.io/hotel-booking-analysis/ retrieved September 17, 2026. The repository contained only index.html. The linked analysis_queries.sql returned 404. The user confirmed they do not have the original dataset or notebook. This revision does not substitute an external version or claim to reconstruct the original extraction.

All findings are descriptive calculations of the published summaries. No individual booking model, causal effect, occupancy estimate or actual cancellation-related profit loss can be computed from these tables.

The original page attributes the data to Antonio, Almeida & Nunes (2019), Hotel booking demand datasets, https://doi.org/10.1016/j.dib.2018.11.126. The authors' documentation describes deposit classification using payments before arrival or cancellation: https://pmc.ncbi.nlm.nih.gov/articles/PMC6297060/. That supports checking field timing, rather than the old page's unsupported assertion that the Non Refund result is a known reservation-status artifact. It does not establish why this dashboard's rates are high.

## Reproduce

Python 3.9+ standard library, no dependencies:

```sh
python3 reanalysis.py
```

Reads aggregate-data.json and writes analysis-results.json.

- Estimated cancellations: count × reported cancellation rate / 100. Source rates are rounded to 0.1 percentage point. The count's rounding bound is approximately count × 0.0005, assuming conventional nearest rounding. This is not a confidence interval.
- Cancellation shares: estimated segment cancellations / estimated cancellations summed over displayed segments. The two missing records are excluded from this denominator.
- Lead-time standardization: pooled shares across City and Resort form the common weights. Each property's rates are weighted by those shares. Observed rates are recomputed with property-specific weights, so tiny differences from headline percentages are expected. This is adjustment for four broad bands only.
- The source label 100+ has sort key 101 and follows 31–100. The text explains this likely 101+ interpretation without claiming verified SQL logic.
- Seasonal normalization: divide July and August counts by three and other months by two, conditional on complete stated date coverage. This does not correct for month lengths, changes across years, supply or selection of non-canceled bookings. The monthly filter is unknown; its similarity to non-canceled totals is an inference only.
- Revenue per listed booking: published channel revenue / listed channel count. The numerator definition is unverified, and the denominator includes the listed canceled bookings. Do not interpret as room rate, contribution profit or causal channel value.
- CAD values retain the original 1.61 factor for consistency only, not as a verified August 2026 exchange rate.

## Calculator

For N bookings, an absolute cancellation-rate reduction d in percentage points, value V per prevented cancellation and contact cost C per booking:

Expected fewer cancellations = N × d / 100
Expected net value = N × (d / 100 × V − C)
Break-even reduction = 100 × C / V percentage points, if V > 0

At the default Both Hotels / Online TA setting, N = 56,477, d = 2, V = CA$100 and C = CA$1. Expected fewer cancellations = 1,129.54; net value = CA$56,477; break-even = 1 percentage point. These defaults are illustrative assumptions, not estimates. V must include resale, service-cost and deposit/refund effects. C should include setup costs allocated per contacted booking. The cohort is historical and is not a forecast of future volume. Negative or nonnumeric inputs and reductions above the baseline rate are rejected; zero-value cases are handled explicitly.

## Publication

Open index.html, or serve this directory with `python3 -m http.server 8767`.

Upload all six deliverable files to the root of the **hotel-booking-analysis** repository. Replace that repository's index.html, not the main portfolio's index.html. Chart.js is included locally with its license header. Google Fonts can fall back to system fonts.

The downloadable script and data replace the broken original SQL link; they do not purport to be the missing original SQL queries.
