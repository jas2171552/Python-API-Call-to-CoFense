# Python-API-Call-to-CoFense
Connects to the vendor CoFense and retrieves data and writes to CSV file

The process contains a variable for output path.  It will also ask if you want to change it during run.

You will need your token from your user profile at CoFense.  The process will ask you for your token at run as well.

The process will loop 3 times in case of error.  The only error I receive is HTTP Forbidden and it is always due to a cooldown timer from CoFense.  Usually waiting 30 seconds and retrying clears the error, which the process does.
