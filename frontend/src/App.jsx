import { useState } from "react"
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts"

const API = "https://ai-analist.onrender.com" //change add render one 

function App() {
  const [queryLoading, setQueryLoading] = useState(false)
  const [queryAnswer, setQueryAnswer] = useState("")
  const [file, setFile] = useState(null)
  const [query, setQuery] = useState(
    "Forecast Total Profit for the next 3 months"
  )

  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleFileChange = (e) => {
    const selected = e.target.files[0]

    if (!selected) return

    if (!selected.name.endsWith(".csv")) {
      setError("Please select a CSV file.")
      return
    }

    setFile(selected)
    setError("")
    setResult(null)
  }

  const analyzeCSV = async () => {
    if (!file) {
      setError("Please select a CSV file first.")
      return
    }

    setLoading(true)
    setError("")
    setResult(null)

    try {
      const formData = new FormData()

      formData.append("file", file)

      // Change this field name only if your FastAPI endpoint
      // expects something other than "file".
      formData.append("query", query)

      const response = await fetch(`${API}/upload_file/`, {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.")
      }

      setResult(data)
    } catch (err) {
      console.error(err)
      setError(err.message || "Something went wrong.")
    } finally {
      setLoading(false)
    }
  }

  const downloadSample = () => {
    window.open(`${API}/sample-data`, "_blank")
  }

  /*
   * Current backend gives predictions as:
   *
   * predictions: [401170, 54882, ...]
   *
   * Until backend sends actual forecast dates,
   * we label them Forecast 1, Forecast 2, etc.
   */
  const predictionData =
    result?.predictions?.map((value, index) => ({
      period: `Forecast ${index + 1}`,
      profit: Number(value),
    })) || []

  const featureData = Object.entries(
    result?.feature_selection?.feature_importance || {}
  )
    .sort((a, b) => b[1] - a[1])
    .map(([name, value]) => ({
      feature: name,
      importance: Number((value * 100).toFixed(2)),
    }))

  /*
   * If your backend later returns historical financial data,
   * plug it into this array.
   */
  const financialData =
    result?.financial_data?.map((item) => ({
      period: item.period,
      revenue: item.revenue,
      cost: item.cost,
      profit: item.profit,
    })) || []

  const training = result?.training
  const askQuestion = async () => {
    if (!result || !query.trim()) return

    setQueryLoading(true)
    setQueryAnswer("")
    setError("")

    try {
      const response = await fetch(`${API}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query.trim(),

          // Send an identifier later.
          // For now we send the analysis context.
          analysis: result,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Query failed.")
      }

      setQueryAnswer(data.answer)
    } catch (err) {
      console.error(err)
      setError(err.message || "Unable to answer query.")
    } finally {
      setQueryLoading(false)
    }
  }
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">

      {/* HEADER */}

      <header className="border-b border-zinc-800 bg-zinc-950/90 backdrop-blur">
        <div className="mx-auto max-w-7xl px-4 py-5 sm:px-6 lg:px-8">

          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">

            <div>
              <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
                CSV Company Analyst
              </h1>

              <p className="mt-1 text-sm text-zinc-400">
                Business intelligence powered by machine learning
              </p>
            </div>

            <div className="rounded-full border border-zinc-800 bg-zinc-900 px-3 py-1 text-xs text-zinc-400">
              ML Analytics
            </div>

          </div>

        </div>
      </header>


      <main className="mx-auto max-w-7xl space-y-6 px-4 py-6 sm:px-6 lg:px-8">


        {/* UPLOAD + QUERY */}

        <section className="grid gap-6 lg:grid-cols-2">

          {/* UPLOAD */}

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-5 shadow-xl sm:p-7">

            <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-indigo-400">
              Dataset
            </p>

            <h2 className="text-xl font-semibold">
              Upload your CSV
            </h2>

            <p className="mt-2 text-sm text-zinc-400">
              Upload a business dataset and let the pipeline analyze it.
            </p>


            <label
              htmlFor="csv-upload"
              className="mt-6 flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-zinc-700 bg-zinc-950/60 px-5 py-10 text-center transition hover:border-indigo-500 hover:bg-zinc-950"
            >

              <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-indigo-500/10 text-2xl">
                ↑
              </div>

              <p className="font-medium">
                {file ? file.name : "Choose a CSV file"}
              </p>

              <p className="mt-1 text-xs text-zinc-500">
                CSV files only
              </p>

              <input
                id="csv-upload"
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="hidden"
              />

            </label>


            <div className="mt-4 flex flex-col gap-3 sm:flex-row">

              <button
                onClick={analyzeCSV}
                disabled={!file || loading}
                className="flex-1 rounded-xl bg-indigo-500 px-5 py-3 font-semibold text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-40"
              >
                {loading ? "Analyzing..." : "Analyze CSV"}
              </button>

              <button
                onClick={downloadSample}
                className="rounded-xl border border-zinc-700 px-5 py-3 font-medium text-zinc-300 transition hover:border-zinc-500 hover:bg-zinc-800"
              >
                Download Sample
              </button>

            </div>

          </div>


          {/* QUERY */}

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-5 shadow-xl sm:p-7">

            <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-indigo-400">
              Ask the analyst
            </p>

            <h2 className="text-xl font-semibold">
              What do you want to know?
            </h2>

            <p className="mt-2 text-sm text-zinc-400">
              Describe the business question you want the model to answer.
            </p>


            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              rows={6}
              placeholder="Example: Forecast total profit for the next 3 months"
              className="mt-6 w-full resize-none rounded-xl border border-zinc-700 bg-zinc-950 p-4 text-sm text-zinc-100 outline-none transition placeholder:text-zinc-600 focus:border-indigo-500"
            />
            <button
              onClick={askQuestion}
              disabled={!result || query.trim() === "" || queryLoading}
              className="mt-4 w-full rounded-xl bg-indigo-500 px-5 py-3 font-semibold text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {queryLoading ? "Thinking..." : "Ask Question"}
            </button>
            {queryAnswer && (
              <div className="mt-5 rounded-xl border border-indigo-500/20 bg-indigo-500/5 p-5">

                <p className="text-xs font-semibold uppercase tracking-widest text-indigo-400">
                  Analyst Answer
                </p>

                <p className="mt-3 whitespace-pre-line text-sm leading-7 text-zinc-300">
                  {queryAnswer}
                </p>

              </div>
            )}

            <div className="mt-3 flex flex-wrap gap-2">

              {[
                "Forecast revenue",
                "Forecast profit",
                "Find important drivers",
                "Analyze sales performance",
              ].map((item) => (
                <button
                  key={item}
                  onClick={() => setQuery(item)}
                  className="rounded-full border border-zinc-700 px-3 py-1.5 text-xs text-zinc-400 hover:border-indigo-500 hover:text-zinc-200"
                >
                  {item}
                </button>
              ))}

            </div>

          </div>

        </section>


        {/* ERROR */}

        {error && (
          <div className="rounded-xl border border-red-900/50 bg-red-950/30 px-4 py-3 text-sm text-red-300">
            {error}
          </div>
        )}


        {/* RESULTS */}

        {result && (
          <>

            {/* OVERVIEW */}

            <section className="grid grid-cols-2 gap-3 sm:grid-cols-4">

              <Stat
                label="Rows"
                value={result.rows}
              />

              <Stat
                label="Columns"
                value={result.cols}
              />

              <Stat
                label="Best Model"
                value={result.training?.best_model || "-"}
              />

              <Stat
                label="R²"
                value={
                  result.training?.metrics?.[
                    result.training?.best_model
                  ]?.R2 ?? "-"
                }
              />

            </section>

            <section className="mt-8 rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6">

              <div className="mb-6">
                <p className="text-xs font-semibold uppercase tracking-widest text-indigo-400">
                  ML Pipeline
                </p>

                <h2 className="mt-2 text-2xl font-bold text-white">
                  What our model did
                </h2>

                <p className="mt-2 text-sm text-zinc-400">
                  Automatic data preparation, feature engineering,
                  feature selection and model preprocessing.
                </p>
              </div>


              {/* CLEANING */}

              <div className="mb-4 rounded-xl border border-zinc-800 bg-zinc-950 p-5">

                <div className="flex items-center gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-500/10 text-green-400">
                    ✓
                  </div>

                  <div>
                    <h3 className="font-semibold text-white">
                      Data Cleaning
                    </h3>

                    <p className="text-sm text-zinc-500">
                      Quality checks and automatic cleanup
                    </p>
                  </div>
                </div>

                <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">

                  <div>
                    <p className="text-xs text-zinc-500">
                      Duplicates Removed
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {result.cleaning_report?.duplicates?.duplicates_removed ?? 0}
                    </p>
                  </div>


                  <div>
                    <p className="text-xs text-zinc-500">
                      Missing Values
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {Object.keys(result.cleaning_report?.missing_values || {}).length}
                    </p>
                  </div>


                  <div>
                    <p className="text-xs text-zinc-500">
                      Outlier Columns
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {
                        Object.values(result.cleaning_report?.outliers || {})
                          .filter(x => x.outliers_removed > 0)
                          .length
                      }
                    </p>
                  </div>


                  <div>
                    <p className="text-xs text-zinc-500">
                      Outliers Removed
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {
                        Object.values(result.cleaning_report?.outliers || {})
                          .reduce(
                            (sum, x) => sum + (x.outliers_removed || 0),
                            0
                          )
                      }
                    </p>
                  </div>

                </div>

              </div>


              {/* FEATURE ENGINEERING */}

              <div className="mb-4 rounded-xl border border-zinc-800 bg-zinc-950 p-5">

                <div className="flex items-center gap-3">

                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-500/10 text-green-400">
                    ✓
                  </div>

                  <div>
                    <h3 className="font-semibold text-white">
                      Feature Engineering
                    </h3>

                    <p className="text-xs text-zinc-500">
                      New business and temporal features
                    </p>
                  </div>

                </div>


                <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-3">

                  <div>
                    <p className="text-sm text-zinc-500">
                      Business Features
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {
                        Object.keys(
                          result.feature_report?.business_features || {}
                        ).length
                      }
                    </p>
                  </div>


                  <div>
                    <p className="text-xs text-zinc-500">
                      Date Columns Processed
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {
                        Object.keys(
                          result.feature_report?.datetime_features || {}
                        ).length
                      }
                    </p>
                  </div>


                  <div>
                    <p className="text-xs text-zinc-500">
                      Generated Date Features
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {
                        Object.values(
                          result.feature_report?.datetime_features || {}
                        )
                          .reduce(
                            (sum, x) => sum + (x.generated?.length || 0),
                            0
                          )
                      }
                    </p>
                  </div>

                </div>

              </div>


              {/* FEATURE SELECTION */}

              <div className="mb-4 rounded-xl border border-zinc-800 bg-zinc-950 p-5">

                <div className="flex items-center gap-3">

                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-500/10 text-green-400">
                    ✓
                  </div>

                  <div>
                    <h3 className="font-semibold text-white">
                      Feature Selection
                    </h3>

                    <p className="text-xs text-zinc-500">
                      Removed irrelevant and redundant features
                    </p>
                  </div>

                </div>


                <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">

                  <div>
                    <p className="text-xs text-zinc-500">
                      Target
                    </p>

                    <p className="mt-1 text-sm font-semibold text-white">
                      {result.feature_selection?.target?.target || "—"}
                    </p>
                  </div>


                  <div>
                    <p className="text-xs text-zinc-500">
                      Features
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {result.feature_selection?.target?.feature_count ?? 0}
                    </p>
                  </div>


                  <div>
                    <p className="text-xs text-zinc-500">
                      ID Columns Removed
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {
                        result.feature_selection?.id_columns?.removed?.length ?? 0
                      }
                    </p>
                  </div>


                  <div>
                    <p className="text-xs text-zinc-500">
                      Correlated Removed
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {
                        result.feature_selection?.correlation?.removed?.length ?? 0
                      }
                    </p>
                  </div>

                </div>

              </div>


              {/* PREPROCESSING */}

              <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-5">

                <div className="flex items-center gap-3">

                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-500/10 text-green-400">
                    ✓
                  </div>

                  <div>
                    <h3 className="font-semibold text-white">
                      Model Preprocessing
                    </h3>

                    <p className="text-xs text-zinc-500">
                      Encoding, scaling and train/test split
                    </p>
                  </div>

                </div>


                <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">

                  <div>
                    <p className="text-xs text-zinc-500">
                      Encoded Columns
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {
                        result.preprocessing?.encoding?.encoded_columns?.length ?? 0
                      }
                    </p>
                  </div>


                  <div>
                    <p className="text-xs text-zinc-500">
                      Final Features
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {
                        result.preprocessing?.encoding?.new_feature_count ?? 0
                      }
                    </p>
                  </div>


                  <div>
                    <p className="text-xs text-zinc-500">
                      Training Samples
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {
                        result.preprocessing?.split?.train_samples ?? 0
                      }
                    </p>
                  </div>


                  <div>
                    <p className="text-xs text-zinc-500">
                      Test Samples
                    </p>

                    <p className="mt-1 text-lg font-semibold text-white">
                      {
                        result.preprocessing?.split?.test_samples ?? 0
                      }
                    </p>
                  </div>

                </div>

              </div>

            </section>

            {/* MODEL PERFORMANCE */}

            {training && (
              <section className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-5 sm:p-7">

                <SectionTitle
                  eyebrow="MODEL"
                  title="Model Performance"
                />

                <div className="mt-6 grid gap-4 md:grid-cols-2">

                  {Object.entries(training.metrics || {}).map(
                    ([model, metrics]) => {

                      const best =
                        model === training.best_model

                      return (
                        <div
                          key={model}
                          className={`rounded-xl border p-5 ${best
                            ? "border-indigo-500 bg-indigo-500/5"
                            : "border-zinc-800 bg-zinc-950/40"
                            }`}
                        >

                          <div className="flex items-center justify-between">

                            <h3 className="font-semibold">
                              {model}
                            </h3>

                            {best && (
                              <span className="rounded-full bg-indigo-500/10 px-2 py-1 text-xs text-indigo-400">
                                Best
                              </span>
                            )}

                          </div>

                          <div className="mt-5 grid grid-cols-3 gap-3">

                            <Metric
                              label="R²"
                              value={metrics.R2}
                            />

                            <Metric
                              label="MAE"
                              value={formatNumber(metrics.MAE)}
                            />

                            <Metric
                              label="RMSE"
                              value={formatNumber(metrics.RMSE)}
                            />

                          </div>

                        </div>
                      )
                    }
                  )}

                </div>

              </section>
            )}


            {/* FEATURE IMPORTANCE */}

            {featureData.length > 0 && (
              <section className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-5 sm:p-7">

                <SectionTitle
                  eyebrow="FEATURE ANALYSIS"
                  title="Important Business Drivers"
                />

                <div className="mt-6 h-[350px] w-full sm:h-[420px]">

                  <ResponsiveContainer width="100%" height="100%">

                    <BarChart
                      data={featureData}
                      layout="vertical"
                      margin={{
                        left: 20,
                        right: 20,
                      }}
                    >

                      <CartesianGrid
                        strokeDasharray="3 3"
                        stroke="#27272a"
                      />

                      <XAxis
                        type="number"
                        stroke="#71717a"
                      />

                      <YAxis
                        dataKey="feature"
                        type="category"
                        width={120}
                        stroke="#a1a1aa"
                        tick={{ fontSize: 11 }}
                      />

                      <Tooltip
                        contentStyle={{
                          background: "#18181b",
                          border: "1px solid #3f3f46",
                          borderRadius: "10px",
                        }}
                      />

                      <Bar
                        dataKey="importance"
                        fill="#6366f1"
                        radius={[0, 6, 6, 0]}
                      />

                    </BarChart>

                  </ResponsiveContainer>

                </div>

              </section>
            )}


            {/* PREDICTIONS */}

            {predictionData.length > 0 && (
              <section className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-5 sm:p-7">

                <SectionTitle
                  eyebrow="PREDICTIONS"
                  title="Profit Forecast"
                />

                <div className="mt-6 h-[300px] w-full sm:h-[420px]">

                  <ResponsiveContainer width="100%" height="100%">

                    <LineChart data={predictionData}>

                      <CartesianGrid
                        strokeDasharray="3 3"
                        stroke="#27272a"
                      />

                      <XAxis
                        dataKey="period"
                        stroke="#71717a"
                      />

                      <YAxis
                        stroke="#71717a"
                        tickFormatter={(value) =>
                          `${Math.round(value / 1000)}k`
                        }
                      />

                      <Tooltip
                        formatter={(value) =>
                          [`$${formatNumber(value)}`, "Predicted Profit"]
                        }
                        contentStyle={{
                          background: "#18181b",
                          border: "1px solid #3f3f46",
                          borderRadius: "10px",
                        }}
                      />

                      <Line
                        type="monotone"
                        dataKey="profit"
                        stroke="#818cf8"
                        strokeWidth={3}
                        dot={{ r: 4 }}
                      />

                    </LineChart>

                  </ResponsiveContainer>

                </div>

                <p className="mt-3 text-xs text-zinc-500">
                  Forecast periods will be replaced with actual dates once
                  the backend returns forecast dates.
                </p>

              </section>
            )}


            {/* REVENUE COST PROFIT */}

            {financialData.length > 0 && (
              <section className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-5 sm:p-7">

                <SectionTitle
                  eyebrow="FINANCIALS"
                  title="Revenue, Cost & Profit"
                />

                <div className="mt-6 h-[320px] w-full sm:h-[420px]">

                  <ResponsiveContainer width="100%" height="100%">

                    <LineChart data={financialData}>

                      <CartesianGrid
                        strokeDasharray="3 3"
                        stroke="#27272a"
                      />

                      <XAxis
                        dataKey="period"
                        stroke="#71717a"
                      />

                      <YAxis
                        stroke="#71717a"
                        tickFormatter={(value) =>
                          `${Math.round(value / 1000)}k`
                        }
                      />

                      <Tooltip
                        formatter={(value) =>
                          `$${formatNumber(value)}`
                        }
                        contentStyle={{
                          background: "#18181b",
                          border: "1px solid #3f3f46",
                          borderRadius: "10px",
                        }}
                      />

                      <Legend />

                      <Line
                        type="monotone"
                        dataKey="revenue"
                        stroke="#818cf8"
                        strokeWidth={2}
                      />

                      <Line
                        type="monotone"
                        dataKey="cost"
                        stroke="#f59e0b"
                        strokeWidth={2}
                      />

                      <Line
                        type="monotone"
                        dataKey="profit"
                        stroke="#22c55e"
                        strokeWidth={3}
                      />

                    </LineChart>

                  </ResponsiveContainer>

                </div>

              </section>
            )}


            {/* AI SUMMARY */}

            {result.business_summary && (
              <section className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-5 sm:p-7">

                <SectionTitle
                  eyebrow="AI ANALYSIS"
                  title="Business Summary"
                />

                <div className="mt-6 whitespace-pre-line rounded-xl bg-zinc-950/60 p-5 text-sm leading-7 text-zinc-300 sm:text-base">
                  {result.business_summary}
                </div>

              </section>
            )}

          </>
        )}

      </main>

    </div>
  )
}


/* COMPONENTS */

function Stat({ label, value }) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/70 p-4 sm:p-5">
      <p className="text-xs uppercase tracking-wide text-zinc-500">
        {label}
      </p>

      <p className="mt-2 truncate text-lg font-bold sm:text-xl">
        {value}
      </p>
    </div>
  )
}


function Metric({ label, value }) {
  return (
    <div>
      <p className="text-xs text-zinc-500">
        {label}
      </p>

      <p className="mt-1 text-sm font-semibold">
        {value}
      </p>
    </div>
  )
}


function SectionTitle({ eyebrow, title }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-widest text-indigo-400">
        {eyebrow}
      </p>

      <h2 className="mt-1 text-2xl font-bold">
        {title}
      </h2>
    </div>
  )
}


function formatNumber(value) {
  if (value === undefined || value === null) return "-"

  return Number(value).toLocaleString("en-IN", {
    maximumFractionDigits: 2,
  })
}

export default App