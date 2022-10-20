from dash import dcc

app2_aim = dcc.Markdown(
    """
    Changes in Short Term Interest Rate (STIR) futures can be difficult to 
    visualise by eyeballing a traditional yield curve chart. A better way of seeing
    small changes is though the lens of relative relationships.

    Here we mean futures calendar spreads, and more specifically in this example 
    we mean butterfly trades. Or spread-of-spreads. e.g H1 - 2*M1 + U1.

    Second, standard charting packages all handle individual contract data in the same
    way. Each day serial / quarterly contracts have one less day to expiry (DTE). But what if we wanted to 
    examine a fixed DTE on the curve. Say today, the March expiry is 140 DTE, 
    and you wanted to form a view on whether that contract is cheap 
    or not. Well if there is any steepness to the curve, simply 
    looking at a chart of the contract will not suffice. But by interpolating the data
    we can create a synthetic constant maturity curve. Then we can compare the fixed DTE 
    butterflys to, say, the price of the middle leg.

    Finally, let's take a look at where our structure is vs. where is was and where it's heading to see if there is any positive roll.

     

    
    """
)
app2_explainer = dcc.Markdown(
    """
    1. So first up in the chart below we have a chart of the futures butterflys down the curve. 
    Use the dropdown to select the span of the butterfly you wish to investigate.

    2. Are there any outliers here? Click on one of the points on the curve below to 
    dig a bit deeper.

    3. Moving on to the scatter plot to the right. Use the slider to add in or remove more 
    data points. These are daily settlement prices.

    4. The chart in the bottom right is showing the two flys on either side of
    the one you are investigating, +/- 90 days.

    NOTE this is an intentionally basic demo. The sample data requuires more preparation, and processing
     before any useful insight can be gained.
    
    """
)
app3_aim = dcc.Markdown(
    """
    This tool was created to help a colleague who uses Excel for backtesting. Often practitioners focus
    on very specific times of the trading session. And a lot of the data we ingest is wasting memory. Excel
     does not handle this well, and is limited in the size of the 
    files it can handle.

    Aims:   
    1. Reduce working file size.
    2. Automatically handle daylight savings.
    3. Speed up the data prepararation time.

    So here we have an application to ingest a .csv file (a sample is pre-loaded, and few options were disabled for the web). 
    Specify our requirements and can select a single, or multiple slices of data. 
    
    We can specify the timezone of the slice. Useful, for example, when working in UTC but focussed
    on the US cash market open. If we select the timezone for the US cash open slice in 'America/Chicago' 
    timezone we will get the correct data, adjusted for daylight savings.

    
    """
)
app3_explainer = dcc.Markdown(
    """
    1. Choose to slice a single file, or all the .csv files in a folder. This feature has not been added to
    the web version. It was intended to be run locally.

    2. Running high / low. This is a useful information to have when slicing data, because once we remove unwanted rows
    we can no longer calculate the session high / low. Period is 24hr. Starting time for this session is required.

    3. Specifying timezones. Useful when we want to examine artefacts that are based on different timezones to
    the datas base timezone. When using timezones, we MUST specify the base data timezone, AND a timezone for
    each slice we take.

    4. Slices. Enter the start_time and end_time for the slice, as well as the interval and timezone (if specified).
    Interval must be greater than the base data, which in this case is a pre-loaded 1m data sample.

    5. Click Submit and it should appear. If not, check you added timezones! Download if required.
    """
)

