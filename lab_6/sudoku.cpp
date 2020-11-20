#include "iostream"
#include "vector"
#include <fstream>
#include <sys/types.h>

using namespace std;

struct Position {
  int row;
  int column;
};

class Grid {

private:
  vector<vector<int>> storage;
  vector<int> input_values;

public:
  void Group(int n) {
    for (size_t i = 0; i < input_values.size(); i = i + n) {

      vector<int> row =
          vector<int>(input_values.begin() + i, input_values.begin() + (i + n));

      storage.push_back(row);
    }
  }

  void ReadFromFile(string &filename) {

    ifstream file(filename);

    char c;
    while (file >> c) {

      if (c == '.') {

        input_values.push_back(0);
      } else {

        int ichar = c - '0';

        input_values.push_back(ichar);
      }
    }
  }

  vector<int> GetRow(Position position) { return storage[position.row]; }
};

int main() {

  Grid grid;
  string filename = "puzzle1.txt";
  grid.ReadFromFile(filename);
  grid.Group(9);

  Position position = {4, 0};
  vector<int> row = grid.GetRow(position);
  for (int values : row) {
    cout << values << " ";
  }

  return 0;
}