# Python-API-Call-to-CoFense
Connects to the vendor CoFense and retrieves data and writes to CSV file

The process contains a variable for output path.  It will also ask if you want to change it during run.

You will need your token from your user profile at CoFense.  The process will ask you for your token at run as well.

The process will loop 3 times in case of error.  The only error I receive is HTTP Forbidden and it is always due to a cooldown timer from CoFense.  Usually waiting 30 seconds and retrying clears the error, which the process does.

Additionally, the process checks the JSON to ensure the fields returned are the expected fields and data types.  When the data is retrieved, it also checks the headers to ensure no changes occured.


Details:

When you connnect to the CoFense API URL, it will return JSON code with a list of all files available.  In this JSON there will include the URL for each file.  This process takes the top row (most recent), parses out the data needed and passes that URL to the next call to retrieve the data.

Opens connection to landing site:
    url = "https://login.phishme.com/api/v1/scenarios.json"
    request = urllib.request.Request(url)
    request.add_header('Authorization', token)
    response = urllib.request.urlopen(request)
    html = response.read()
    
Parses the JSON response to get most current URL for CSV
    y = json.loads(html)
    x = y[0]  #[0] will return the top row

Takes the URL for the most current file and opens connection and exports data
    site= str(x["full_csv_url"])
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    req.add_header('Authorization', token)

    with urlopen(req) as x:
        data = x.read().decode('utf-8')

