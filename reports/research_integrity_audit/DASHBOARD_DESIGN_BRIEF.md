# Dashboard Design Brief — Bold, Interactive and Evidence-Led

**Product:** Poultry Disease Intelligence — Nigeria  
**Design objective:** create a memorable, presentation-quality analytics experience that is easy to explore on desktop and mobile, without sacrificing scientific clarity or accessibility.

## 1. Visual identity

Retain the current deep-navy and teal identity. Use a disciplined colour system rather than unrelated colours on every chart.

| Role | Colour | Use |
|---|---|---|
| Primary navy | #102A43 | Navigation, headings, high-emphasis labels |
| Secondary navy | #163F5C | Secondary panels and dark surfaces |
| Surveillance teal | #0F9D91 | Observed reported counts and primary positive data series |
| Bright blue | #3B82F6 | Geographic and time-series exploration |
| Gold / amber | #F2B84B | Unavailable or incomplete data, caution and attention |
| Coral | #E27662 | Material error, residual and warning states |
| Purple | #8B7CF6 | Secondary comparison series where needed |
| Paper surface | #F4F7FA | Page background |
| White | #FFFFFF | Cards and chart plotting surfaces |

Use a consistent disease palette across all tabs. Pair colour with a disease label and, where practical, line style or marker shape. Never rely on colour alone to communicate observed, missing, warning or disease categories.

## 2. Interaction standard

Every major visual should provide:

- Hover details with state, disease, semester, measure, units and data-status information.
- Click-to-inspect behaviour that opens a compact detail panel or selected-record table.
- Zoom, pan, reset and download controls where the chart type supports them.
- A plain-language explanation describing what the visual shows, the calculation and its limitations.
- Clear denominators and sample sizes for percentages, correlations and model metrics.
- A visible reset or return path after drill-down.

Global filters should update surveillance views consistently. Project-wide quality statistics and saved model-evaluation samples must be explicitly labelled when they are not narrowed by the global filters.

## 3. Core dashboard experience

### Overview
- Strong but compact hero title and one-sentence value proposition.
- KPI cards for source rows, analytical groups, observed counts and reporting availability.
- Separate global-source statistics from the currently selected view.
- Chronological six-month trend with explicit gaps for unavailable periods.
- A small number of high-value supporting charts rather than a crowded grid.

### Exploratory analysis
- Chronologically ordered trends with disease-specific colours and gaps not connected across missing periods.
- Histograms, box plots and robust distribution summaries.
- Relationship explorer with selectable measure, linear/log scale, trendline, correlation, sample size and outlier detail.
- Climate relationships kept separate from predictive claims; display whether climate values are contemporaneous or lagged.

### Geographic intelligence
- Interactive Nigeria ADM1 choropleth built from the validated geoBoundaries source.
- State click opens a profile with reporting completeness, disease coverage, six-month history and source records.
- Two distinct map modes: observed reported counts and numeric-reporting completeness.
- Country-level aggregates and unknown geography excluded from ADM1 colouring and clearly disclosed.
- Avoid risk/prevalence language unless population denominators and an epidemiologically validated risk method are added.

### Forecasting
- Separate retrospective model results from prospective forecasts.
- Show selected method, forecast issue time, target semester, prediction unit, uncertainty range and historical data coverage.
- Compare the selected method against simple baselines on the same rows.
- Provide a plain-language explanation and limitations for every forecast.
- Do not display an operational alert or risk score until a prospective model and decision threshold have been validated with animal-health users.

### Data quality and methods
- A missingness/status heatmap that distinguishes observed, confirmed absent and unknown only when each is supported by source data.
- Ambiguous source measures and multi-row consolidation rules documented visibly.
- Clickable research-stage walkthrough showing method, reason, evidence and outstanding limitations.

### Share and QR
- Display a QR code only after the app has a verified public HTTPS URL.
- Test the URL and QR on at least one mobile device and one desktop browser.
- Provide a readable short URL alongside the QR code.

## 4. Accessibility and responsive behaviour

- Design towards WCAG 2.2 AA contrast and interaction expectations.
- Use semantic headings, clear labels, visible focus, keyboard-accessible filters and controls, and meaningful chart descriptions.
- Ensure tables have readable headers and remain usable on narrow screens.
- Stack chart columns on mobile rather than shrinking charts into unreadable miniatures.
- Check the map has a usable alternative state selector/table for people unable to interact with the map.

## 5. Visual acceptance tests

Before release, verify at minimum:

1. Default overview at desktop and narrow/mobile widths.
2. One disease filter and one state filter update the intended surveillance visuals.
3. Clicking a time-series point and a geographic state opens the correct record details.
4. Missing periods remain visible as gaps, not zero-valued bars or connected lines.
5. A missing target never appears as a confirmed absence.
6. Climate charts identify the temporal relationship to the outbreak target.
7. Forecast views state their prediction issue time and target period.
8. Tooltips, legends, colour contrast, text sizing and keyboard focus remain clear.
9. Public URL and QR code open the complete dashboard without requiring the developer's local machine.