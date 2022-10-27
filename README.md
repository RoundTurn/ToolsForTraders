# Tools for Traders

### Overview

A range of timeseries tools for financial traders. Apologies if some of the language is unclear, the content is relevant to financial futures traders. 
This is a personal project to demonstrate some coding. Presented as a multi-page Dash / Plotly web application. It brings together a few pieces I have worked on professionally.
Hosted on free Heroku account, initial load speed can be sub-optimal.

### Contents
<ol>
  <li>Constant Maturity STIR Visualisation app.
    <ul>
      <li>Manual interpolation of STIR futures data to create constant maturity curve on a sample of Short Term Interest Rate futures.</li>
      <li>This is a Python interpretation of an old tool I built in Excel. </li>
      <li>There are a few filters that must be applied to the raw futures data before this becomes a useful tool. My aim here was to demonstrate some visualisations whilst I practised callbacks in Dash.</li>
    </ul>
  </li>
  <li>Time Slicing.
    <ul>
      <li>A simplified demonstration of a desktop app I built for a hedge fund trader. He worked on Excel and was struggling to handle larger timeseries files. He worked on very specific periods of the trading day, and wanted to reduce the file size by removing the excess data. Not something easily done in Excel.</li>
      <li>Lot of Pandas work!</li>
    </ul>
  </li>
  <li>Relative Value Curves.
    <ul>
      <li>This is (was) actually one of my favourite trades as a professional futures trader. Trading the steepness of the Australian bond futures curve against the steepness of the US bond futures curve. Quite a mouthful.</li>
      <li>Built in Jupyter Notebook, more use of Pandas and a fair amount of timezones. I use BackTrader for backtesting in this example. Which is a very feature-rich platform, but not something I use today.</li>
      <li>It’s a mean reversion trade, with the usual caveats for this type of strategy.</li>
      <li>This is not a retail trade, it requires direct market access because a lot of the real-world magic comes from trade execution. With it being a 4-leg trade, you don’t want to be crossing the bid/ask.</li>
    </ul>
  </li>
</ol>

### Help!

If you have any questions regarding the content, please feel free to comment / ask questions. I will help where I can.


