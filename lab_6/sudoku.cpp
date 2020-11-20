#include "iostream"
#include "vector"
#include <fstream>
#include <sys/types.h>
#include <type_traits>
#include <algorithm>

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

  vector<int> GetColumn(Position position) {

    vector<int> result;

    for (vector<int> row : storage) {

      result.push_back(row[position.column]);
    }

    return result;
  }

  vector<int> GetBlock(Position position) {

    int x_start = (position.row / 3) * 3;
    int y_start = (position.column / 3) * 3;


    vector<int> result;

    for (int row_index = x_start; row_index < x_start + 3; row_index++) {

      vector<int> row = storage[row_index];
      vector<int> slice =
          vector<int>(row.begin() + y_start, row.begin() + (y_start + 3));

      for (int value : slice) {
        result.push_back(value);
      }
    }
    return result;
  }

  template <typename T> T FindEmptyPosistions() {

    for (size_t row_index = 0; row_index < storage.size(); row_index++) {

      vector<int> row = storage[row_index];
      for (size_t column_index = 0; column_index < row.size(); column_index++) {

        int value = row[column_index];
        if (value == 0) {
          Position pos = {static_cast<int>(row_index),
                          static_cast<int>(column_index)};
          return pos;
        }
      }
    }
    return false;
  }

  vector<int> FindPossibeValues(Position position){

    vector<int> taken;

    vector<int> row = GetRow(position);
    vector<int> column = GetColumn(position);
    vector<int> block = GetBlock(position);

    taken.insert(taken.end(), row.begin(), row.end());
    taken.insert(taken.end(), column.begin(), column.end());
    taken.insert(taken.end(), block.begin(), block.end());

    sort(taken.begin(), taken.end());
    unique(taken.begin(), taken.end());
    return taken;



  }
};

int main() {

  Grid grid;
  string filename = "puzzle1.txt";
  grid.ReadFromFile(filename);
  grid.Group(9);

  Position position = {0, 0};
  vector<int> row = grid.FindPossibeValues(position);
  for (int value : row) {
    cout << value << " ";
  }

  return 0;
}