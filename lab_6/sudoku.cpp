#include "iostream"
#include "vector"
#include <fstream>

using namespace std;

class Grid {

private:
  vector<vector<int>> storage;

public:
  void ReadFromFile(string &filename) {

    vector<int> full_data;
    ifstream file(filename);

    char c;
    while (file >> c) {

      if (c == '.') {

        full_data.push_back(0);
      } else {

        int ichar = c - '0';

        full_data.push_back(ichar);
      }
    }

    cout << full_data.size() << endl;
    for (int value : full_data) {
      cout << value << endl;
    }
  }
};

int main() {

  Grid grid;
  string filename = "puzzle1.txt";
  grid.ReadFromFile(filename);

  return 0;
}