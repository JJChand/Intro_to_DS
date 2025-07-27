from AlgoAPI import AlgoAPIUtil, AlgoAPI_Backtest

class AlgoEvent:
    def __init__(self):
        # --- Strategy Parameters ---
        # 1. Define the trading universe
        self.instrument_list = ["SPY", "QQQ", "IWM", "EFA", "EEM", "GLD", "USO"]
        
        # 2. Set the lookback period for momentum calculation (in days)
        self.lookback_period = 120  # Approx. 6 months
        
        # 3. Set the rebalancing frequency (in days)
        self.rebalance_period = 20  # Approx. 1 month
        
        # 4. Define how many assets to long and short
        self.hold_N_assets = 2
        
        # --- System Variables ---
        self.evt = None
        self.rebalance_counter = 0
        self.historical_data = {} # Dictionary to store price history for each instrument

    def start(self, mEvt):
        """
        This function is called once at the start of the backtest.
        """
        self.evt = AlgoAPI_Backtest.AlgoEvtHandler(self, mEvt)
        self.evt.start()

        # Initialize the historical data dictionary for our universe
        for instrument in self.instrument_list:
            self.historical_data[instrument] = []
        
        self.evt.log(f"Strategy Started. Universe: {self.instrument_list}, Lookback: {self.lookback_period} days.")

    def on_bulkdatafeed(self, isSync, bd, ab):
        """
        This function is called at the start to load historical data in bulk.
        We use it to pre-fill our lookback window.
        """
        self.evt.log("Processing bulk data to pre-fill historical prices...")
        if isSync:
            for instrument in self.instrument_list:
                if instrument in bd:
                    # Store the 'close' price from each historical bar
                    for bar in bd[instrument]:
                        self.historical_data[instrument].append(bar['close'])
            self.evt.log("Bulk data loading complete.")
            
    def on_marketdatafeed(self, md, ab):
        """
        This function is called for every new piece of market data (every day in our case).
        This is the main engine of the strategy.
        """
        # Append the latest closing price to our historical data
        instrument = md.instrument
        if instrument in self.historical_data:
            self.historical_data[instrument].append(md.close)

        # --- Rebalancing Trigger ---
        # To ensure rebalancing logic runs only ONCE per day, we tie the counter
        # to the data feed of the first instrument in our list.
        if instrument == self.instrument_list[0]:
            self.rebalance_counter += 1

        # If it's not time to rebalance, do nothing.
        if self.rebalance_counter < self.rebalance_period:
            return

        # --- Rebalancing Day Logic ---
        self.evt.log(f"--- Rebalancing Day on {self.evt.getCurrentDate()} ---")
        self.rebalance_counter = 0  # Reset the counter for the next cycle

        # Check if we have enough historical data to calculate momentum
        for inst in self.instrument_list:
            if len(self.historical_data[inst]) < self.lookback_period:
                self.evt.log(f"Not enough data for {inst} ({len(self.historical_data[inst])} days). Skipping rebalance.")
                return # Wait for more data before trading

        # --- 1. Calculate Momentum ---
        momentum_scores = {}
        for inst in self.instrument_list:
            prices = self.historical_data[inst]
            # Momentum = (Current Price / Price N periods ago) - 1
            # A simple return over the lookback period
            momentum = (prices[-1] / prices[-self.lookback_period]) - 1
            momentum_scores[inst] = momentum
            
        # --- 2. Rank Instruments ---
        # Sort instruments by their momentum score, from highest to lowest
        ranked_instruments = sorted(momentum_scores.items(), key=lambda item: item[1], reverse=True)
        
        # --- 3. Determine Long, Short, and Flat Positions ---
        longs = [item[0] for item in ranked_instruments[:self.hold_N_assets]]
        shorts = [item[0] for item in ranked_instruments[-self.hold_N_assets:]]
        
        # Any instrument not in the long or short list should be flat (position closed)
        flats = [inst for inst in self.instrument_list if inst not in longs and inst not in shorts]
        
        self.evt.log(f"Top performers (Long): {longs}")
        self.evt.log(f"Bottom performers (Short): {shorts}")
        self.evt.log(f"Closing positions in: {flats}")
        
        # --- 4. Execute Trades ---
        portfolio_value = self.evt.getPortfolio().getPortfolioValue()
        num_positions = len(longs) + len(shorts)
        
        if num_positions == 0:
            return # Should not happen with this logic, but good practice
            
        capital_per_position = portfolio_value / num_positions
        
        # Close out positions we no longer want
        for inst in flats:
            # Send an order to set the target position for this instrument to 0 shares
            self.evt.sendOrder(inst, 0, "MKT", 0, "TARGET_SHARES")

        # Place orders for long positions
        for inst in longs:
            last_price = self.historical_data[inst][-1]
            target_quantity = capital_per_position / last_price
            self.evt.sendOrder(inst, target_quantity, "MKT", 0, "TARGET_SHARES")
            
        # Place orders for short positions
        for inst in shorts:
            last_price = self.historical_data[inst][-1]
            # Note the negative sign for shorting
            target_quantity = - (capital_per_position / last_price)
            self.evt.sendOrder(inst, target_quantity, "MKT", 0, "TARGET_SHARES")


    def on_orderfeed(self, of):
        """
        This function is called when there is an update on one of our orders.
        We can use it for logging and debugging.
        """
        if of.is_filled:
            self.evt.log(f"FILLED: {of.instrument} - {of.fill_volume} shares @ {of.fill_price}")
        elif of.is_rejected:
            self.evt.log(f"REJECTED: {of.instrument} - Reason: {of.rejected_reason}")

    # --- Unused Event Handlers ---
    # We leave these empty as our strategy does not use this data.
    def on_newsdatafeed(self, nd):
        pass

    def on_econsdatafeed(self, ed):
        pass
        
    def on_weatherdatafeed(self, wd):
        pass

    def on_corpAnnouncement(self, ca):
        pass