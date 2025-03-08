# Applying Nuclear Physics to Key Career Decisions: Monte Carlo in Real Life

## How to Run the Code on Mac

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python script.py
```

Running the above commands should produce an output similar to, but not identical to, the below:

```
┌────────────┬──────────┬────────────┬──────────┬──────────┐
│ scenario   ┆ mean_NPV ┆ median_NPV ┆ p5_NPV   ┆ p95_NPV  │
│ ---        ┆ ---      ┆ ---        ┆ ---      ┆ ---      │
│ str        ┆ f64      ┆ f64        ┆ f64      ┆ f64      │
╞════════════╪══════════╪════════════╪══════════╪══════════╡
│ scenario_a ┆ 2.2922e6 ┆ 2.2910e6   ┆ 2.0639e6 ┆ 2.5294e6 │
│ scenario_b ┆ 1.5112e6 ┆ 1.5113e6   ┆ 1.2371e6 ┆ 1.7864e6 │
└────────────┴──────────┴────────────┴──────────┴──────────┘
```
This sample output is showing that given the current assumptions codified in script.py, scenario A is expected to have a higher NPV than scenario B. The NPV for scenario A is expected to be 2.29 million dollars over the next five years; while scenario B's assumptions describe 1.51 million dollars of Net Present Value.

## Original Blog Post on Medium

Recently I was on the phone with an old friend of mine, and he shared a problem I empathized with immensely. He had been presented with a new job opportunity that would confer a substantial raise, as well as a substantial increase in demands on his time, and was having a lot of difficulty estimating the costs and benefits of accepting the offer. 

Not long before, he and his wife learned they were pregnant, and not long before that he had conceived of an idea for a side hustle which he felt might be quite lucrative. Like so many, he wanted to build a bright future for his wife and kid. And on the surface, the decision before him seemed straightforward: take the new job and sacrifice the side hustle for at least a few years, or decline the offer and see where entrepreneurship took him. 

But bubbling under the surface of these two clear paths were a thousand moving parts, a complex tapestry of interwoven variables. How would changing healthcare benefits, paternity leave, equity grants, tax regimes, and not least of all the opportunity cost of the side hustle cash flow impact his future ability to provide his kid with a robust education? My friend and his wife were overwhelmed with the decision and unsure where to start.

My favorite ideas usually come from the most unexpected places. In one job over a decade ago, I was tasked with improving the accuracy of a business forecast estimating day-by-day demand for service technicians in geographies across the United States. One day I happened across a webinar describing how wind turbine farms can estimate demand for their electricity production using neural networks, a mathematical model derived from how the human brain is believed to reason, and I knew I had landed on something powerful. Borrowing from that seemingly unrelated domain to this one, I built a proof-of-concept neural network in Matlab (an academic software my university had given me) showing order of magnitude improvement in the forecast accuracy, driving meaningful business outcomes by rightsizing staffing levels and decreasing overtime.

Similarly, as my friend described his conundrum, I was reminded of two scientists laboring away in the Manhattan Project during World War II. Asked to predict key behaviors of the atomic weapon, the scientists were finding the problem to be intractable for their traditional mathematical procedures. One of the scientists, Stanisław Ulam, had himself just been recovering from an illness and playing a lot of solitaire during his recovery. He was trying to work out a probability in the game when he stumbled on an idea of using random experiments, or simulations, to guess at the odds. Not long after, he and John von Neumann set out to apply the same technique, which they began to call “Monte Carlo,” to their nuclear work, and the method was so effective that it is widely used today in fields as diverse as manufacturing operations improvement and analysis of complex Wall Street financial derivatives.

Years ago, I had applied Ulam’s “Monte Carlo” technique, as it came to be known, to the study of another friend’s commercial real estate development portfolio and the options available to him, with their various potential financial returns and various potential risks. I knew how potent this technique could be to evaluate uncertain risks and gauge opportunities. And why should nuclear physicists and commercial real estate developers get to have all the fun?! Many tools are available to make Monte Carlo analysis feasible for anyone who has access to an installation of Microsoft Excel or Python.

My friend’s entrepreneurial cash flows presented the most uncertainty. He envisioned doing some free work for a few months while incurring some startup costs, to bolster both his skills and garner early case studies of success he could reference in future sales efforts, then grow into work billed on an hourly basis for a time, before ultimately focusing on selling monthly retainers for his efforts.

I described my friend’s opportunity analysis problem to a Large Language Model, and asked the LLM to build the outline of a Python program featuring Monte Carlo simulation to estimate the Net Present Value (NPV) of each of the two choices available to him. It landed on using the popular numpy library to sample – it chose ten thousand times for each of the two scenarios – from each of the random variables he and I would define (random variables such as how many months of free work, his average hourly rate and hours of billings per month, average monthly retainer size, healthcare premiums incurred in the prospective new job, and so on) and crunch the cash flows resulting from these assumptions month-by-month for the next five years. The LLM further intended to use another Python library, Pandas, for analyzing all the statistics relating to the cash flows, including discounting the cash flows back to today’s dollars. I guided the LLM to use the more modern Polars library instead of Pandas, but otherwise the starting point it provided was robust.

After just two to three hours of changes to the Python code provided by the LLM, I was able to share with my friend a tool into which he could plug some of the assumptions – predominantly the average and standard deviation to use for each of the normally-distributed random variables, in addition to any deterministic drivers – and the tool would output worst-case, base-case, and best-case scenarios for each of the two scenarios. This gave he and his wife a sound mathematical framework on which they could question and tweak assumptions, click a button, and a few seconds later see the impact of those adjustments in the Net Present Value of the cash flows.
