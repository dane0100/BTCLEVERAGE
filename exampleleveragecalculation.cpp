#include <iostream>
#include <iomanip>
#include <cmath>

using namespace std;

int main() {
    // Variables for user input
    double btc_price, mu, volatility, funding_rate, trading_fee, capital;
    double leverage;

    // Get user inputs
    cout << "Enter current BTC price (USD): ";
    cin >> btc_price;
    cout << "Enter expected daily return (mu, as decimal, e.g., 0.005 for 0.5%): ";
    cin >> mu;
    cout << "Enter daily volatility (as decimal, e.g., 0.04 for 4%): ";
    cin >> volatility;
    cout << "Enter daily funding rate (as decimal, e.g., 0.0006 for 0.06%): ";
    cin >> funding_rate;
    cout << "Enter trading fee per trade (as decimal, e.g., 0.001 for 0.1%): ";
    cin >> trading_fee;
    cout << "Enter trading capital (USD): ";
    cin >> capital;
    cout << "Enter desired leverage (e.g., 5 for 5x): ";
    cin >> leverage;

    // Calculate mp (marginal profit after fees and funding)
    double gross_return = mu * leverage; // Gross return with leverage
    double mp = gross_return - trading_fee - funding_rate; // Net return
    if (mp < 0) {
        mp = 0; // Prevent negative returns for simplicity
    }

    // Calculate lambda (mp/mu)
    double lambda = (mu != 0) ? mp / mu : 0;

    // Calculate Kelly Criterion leverage
    double kelly_leverage = (mu - funding_rate) / (volatility * volatility);

    // Calculate position size and liquidation risk
    double position_size = capital * leverage;
    double btc_amount = position_size / btc_price;
    double liquidation_price_drop = (capital / position_size) * btc_price; // Approx liquidation price
    double adverse_move_loss = volatility * btc_price * btc_amount * leverage;
    double net_profit = mp * capital;

    // Output results
    cout << fixed << setprecision(2);
    cout << "\n=== BTC Leverage Trading Analysis ===\n";
    cout << "BTC Price: $" << btc_price << endl;
    cout << "Expected Daily Return (mu): " << (mu * 100) << "%" << endl;
    cout << "Daily Volatility: " << (volatility * 100) << "%" << endl;
    cout << "Position Size: $" << position_size << " (" << btc_amount << " BTC)" << endl;
    cout << "Net Daily Return (mp): " << (mp * 100) << "%" << endl;
    cout << "Optimal Risk Level (lambda): " << lambda << endl;
    cout << "Kelly Criterion Leverage: " << kelly_leverage << "x" << endl;
    cout << "Net Profit for " << (mu * 100) << "% BTC Move: $" << net_profit << endl;
    cout << "Liquidation Price: ~$" << (btc_price - liquidation_price_drop) << " ("
         << (liquidation_price_drop / btc_price * 100) << "% drop)" << endl;
    cout << "Loss from " << (volatility * 100) << "% Adverse Move: $" << adverse_move_loss
         << " (" << (adverse_move_loss / capital * 100) << "% of capital)" << endl;

    // Risk warning
    if (adverse_move_loss > capital) {
        cout << "\nWARNING: A " << (volatility * 100) << "% adverse move risks liquidation!\n";
        cout << "Consider lowering leverage to ~" << kelly_leverage << "x.\n";
    } else {
        cout << "\nRisk level is manageable with current leverage.\n";
    }

    return 0;
}
