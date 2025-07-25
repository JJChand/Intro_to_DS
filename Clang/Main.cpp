#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <string>

using namespace std;

class TicTacToe {
public:
    TicTacToe(int n) : n(n), currentPlayer('X') {
        board.resize(n, vector<vector<char> >(n, vector<char>(n * n, '.')));
        mainGridWinners.resize(n, vector<char>(n, '.'));
    }

    void play() {
        srand(time(0));
        string input;
        
        while (true) {
            int mainX, mainY;
            do {
                mainX = rand() % n;
                mainY = rand() % n;
            } while (mainGridWinners[mainX][mainY] != '.');

            cout << "\nCurrent grid: (" << mainX + 1 << ", " << mainY + 1 << ")\n";
            displayBoard(mainX, mainY);

            cout << "Player " << currentPlayer << ", enter your move (row and column 1 to " << n << ", or 'Quit' to end): ";
            cin >> input;
            
            // Check for quit command
            if (input == "Quit" || input == "quit") {
                cout << "\nGame ended by player. Thanks for playing!\n";
                return;
            }
            
            // Try to parse move
            int subX, subY;
            try {
                subX = stoi(input);  // Convert first input to number
                if (!(cin >> subY)) {    // Read second number
                    cin.clear();
                    cin.ignore(10000, '\n');
                    cout << "Invalid input. Please enter two numbers or 'Quit'.\n";
                    continue;
                }
            } catch (const invalid_argument&) {
                cout << "Invalid input. Please enter two numbers or 'Quit'.\n";
                continue;
            }

            if (isValidMove(mainX, mainY, subX - 1, subY - 1)) {
                board[mainX][mainY][(subX - 1) * n + (subY - 1)] = currentPlayer;
                
                if (checkWin(mainX, mainY)) {
                    displayBoard(mainX, mainY);
                    cout << "Player " << currentPlayer << " wins grid (" << mainX + 1 << "," << mainY + 1 << ")!\n";
                    mainGridWinners[mainX][mainY] = currentPlayer;
                    
                    // Only check for game end if this player has won multiple grids
                    if (checkMainGridWin()) {
                        displayBoard(mainX, mainY);
                        cout << "Player " << currentPlayer << " wins the entire game!\n";
                        return;  // End the game only on main grid win
                    }
                }
                
                togglePlayer();  // Switch players after a valid move
            } else {
                cout << "Invalid move. Try again.\n";
            }
        }
    }

private:
    int n;
    char currentPlayer;
    vector<vector<vector<char> > > board;
    vector<vector<char> > mainGridWinners;

    void togglePlayer() {
        currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
    }

    bool isValidMove(int mainX, int mainY, int subX, int subY) {
        if (mainGridWinners[mainX][mainY] != '.') {
            cout << "This grid has already been won by Player " << mainGridWinners[mainX][mainY] << "!\n";
            return false;
        }
        return subX >= 0 && subY >= 0 && subX < n && subY < n && board[mainX][mainY][subX * n + subY] == '.';
    }

    void displayBoard(int activeMainX, int activeMainY) {
        cout << "\nFull Board (Active grid: " << activeMainX + 1 << "," << activeMainY + 1 << ")\n\n";
        
        // For each row of sub-grids
        for (int mainRow = 0; mainRow < n; mainRow++) {
            // For each row within the sub-grids
            for (int subRow = 0; subRow < n; subRow++) {
                // For each column of sub-grids
                for (int mainCol = 0; mainCol < n; mainCol++) {
                    // Draw the sub-grid row
                    for (int subCol = 0; subCol < n; subCol++) {
                        // Highlight active grid with brackets
                        if (mainRow == activeMainX && mainCol == activeMainY) {
                            cout << "[" << board[mainRow][mainCol][subRow * n + subCol] << "]";
                        } else {
                            cout << " " << board[mainRow][mainCol][subRow * n + subCol] << " ";
                        }
                    }
                    // Add separator between sub-grids
                    if (mainCol < n - 1) cout << " | ";
                }
                cout << endl;
            }
            // Add horizontal separator between rows of sub-grids
            if (mainRow < n - 1) {
                cout << string(n * (n * 3 + 2) - 1, '-') << endl;
            }
        }
        cout << endl;
    }

    bool checkWin(int mainX, int mainY) {
        // Check rows
        for (int i = 0; i < n; ++i) {
            bool win = true;
            for (int j = 0; j < n; ++j) {
                if (board[mainX][mainY][i * n + j] != currentPlayer) {
                    win = false;
                    break;
                }
            }
            if (win) return true;
        }
        
        // Check columns
        for (int j = 0; j < n; ++j) {
            bool win = true;
            for (int i = 0; i < n; ++i) {
                if (board[mainX][mainY][i * n + j] != currentPlayer) {
                    win = false;
                    break;
                }
            }
            if (win) return true;
        }
        
        // Check diagonals
        bool win = true;
        for (int i = 0; i < n; ++i) {
            if (board[mainX][mainY][i * n + i] != currentPlayer) {
                win = false;
                break;
            }
        }
        if (win) return true;
        
        win = true;
        for (int i = 0; i < n; ++i) {
            if (board[mainX][mainY][i * n + (n - 1 - i)] != currentPlayer) {
                win = false;
                break;
            }
        }
        return win;
    }

    bool checkMainGridWin() {
        char player = currentPlayer;
        
        // Check rows of main grid
        for (int i = 0; i < n; ++i) {
            bool win = true;
            for (int j = 0; j < n; ++j) {
                if (mainGridWinners[i][j] != player) {
                    win = false;
                    break;
                }
            }
            if (win) return true;
        }
        
        // Check columns of main grid
        for (int j = 0; j < n; ++j) {
            bool win = true;
            for (int i = 0; i < n; ++i) {
                if (mainGridWinners[i][j] != player) {
                    win = false;
                    break;
                }
            }
            if (win) return true;
        }
        
        // Check diagonals of main grid
        bool win = true;
        for (int i = 0; i < n; ++i) {
            if (mainGridWinners[i][i] != player) {
                win = false;
                break;
            }
        }
        if (win) return true;
        
        win = true;
        for (int i = 0; i < n; ++i) {
            if (mainGridWinners[i][n - 1 - i] != player) {
                win = false;
                break;
            }
        }
        return win;
    }

    bool processInput(string& input, int& x, int& y) {
        try {
            x = stoi(input);
            if (!(cin >> y)) {
                cin.clear();
                cin.ignore(10000, '\n');
                return false;
            }
            return true;
        } catch (const invalid_argument&) {
            return false;
        }
    }
};

int main() {
    int n;
    cout << "Enter the size of the board (n > 3): ";
    cin >> n;
    if (n <= 3) {
        cout << "Invalid size. Exiting.\n";
        return 0;
    }

    TicTacToe game(n);
    game.play();

    return 0;
}
