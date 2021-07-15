import twint
import nest_asyncio

nest_asyncio.apply()

# Configure
c = twint.Config()
c.Output = 'tweets.csv'
c.Store_csv = True
c.Search = "BTC"
c.Since ="2021-07-14"
c.Until = "2021-07-15"

# Run
twint.run.Search(c)