#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <map>

using namespace std;
typedef unsigned long long int ui;
map<string, set<string>> t_dep;//Map with "KEY" as a string and "VALUE" as set of strings which the key is directly dependent upon

void display_set(set<string> vec, string desc = "") {//Function to display a set
	cout << desc;
	for (auto x : vec) {
		cout << x << " ";
	}
	cout << endl;
}
void display_map() {//Function to display a map
	for (auto x : t_dep) {
		cout << "Key : " << x.first << " Dependencies : ";
		display_set(x.second);
	}
}
void add_direct(string values) {// Function to add KEY:String and VALUE: set of direct dependencies to the map
	ui len_val = values.length();// Length of inputted row
	set<string> val;//Temp storage for VALUE of map
	string key = "";//To store Key
	ui index = 0;
	bool not_first_WS_flag = false;// Flag set to true when key is extracted from the input
	while (index < len_val) {//Extract white space seperated tokens
		string temp = "";
		while (values[index] != ' ' && values[index] != '\0') {
			temp += values[index];
			index++;
		}
		if (not_first_WS_flag) {//flag set to true, so the token extracted in a dependency
			val.insert(temp);
		}
		else {//flag still false so the token extracted must be the key
			key = temp;
			not_first_WS_flag = true;//key found, set flag to true
		}
		index++;

		temp = "";//empty temp
	}
	auto k = t_dep.find(key);//if key already exists, add new dependencies to already existing dependency set
	if (k != t_dep.end()) {
		for (auto x : val) {
			k->second.insert(x);
		}
	}
	else {//else add the new pair to the map
		t_dep.insert(pair<string, set<string>>(key, val));
	}
}
set<string> dependencies_for(string key) {//Returns set of dependencies for a given string
	set<string> res;//result set
	auto k = t_dep.find(key);
	if (k != t_dep.end()) {//if key exists, that means user entered a correct value
		for (auto x : k->second) {//generate the set of direct dependecies and add it to result set.
			if (x.compare(k->first) != 0)//if a circle dependency exists, skip insertion
				res.insert(x);
		}
		for (auto x : res) {//now iterate over the result set and keep adding dependencies per member to the same list
			auto inner_k = t_dep.find(x);

			if ((inner_k != t_dep.end())) {
				for (auto y : inner_k->second) {
					if (y.compare(k->first) != 0) {//if a circle dependency exists, skip insertion
						res.insert(y);//since the same list gets appended again and again, every indirect dependency is covered
					}
				}
			}

		}
	}
	return res;
}

void menu() {// Generate menu Items
	cout << endl;
	cout << "**********|Menu|**********\n";
	cout << "Enter choice amongst the following :\n";
	cout << "1) Display Input.\n";
	cout << "2) Find Dependency.\n";
	cout << "3) Exit.\n";
	cout << endl;
}
int main() {
	ui T;
	cout << "Enter the number of lines to treat as input : ";
	cin >> T;
	cin.ignore();

	while (T) {//take T lines of input
		string val;
		getline(cin, val);
		add_direct(val);
		T--;
	}

	bool exit_flag = false;
	while (!exit_flag) {
		menu();
		int cmd;
		cin >> cmd;
		string dep_for = "";
		set<string> str;
		switch (cmd) {//Menu
		case 1:
			display_map();
			break;
		case 2:
			cout << "Enter the String for which you need to find the dependencies : ";
			cin >> dep_for;
			str = dependencies_for(dep_for);
			cout << endl;
			display_set(str, dep_for + " is dependent on :\n");
			cout << endl;
			break;

		case 3:
			exit_flag = true;
			break;

		default:
			cout << "Wrong choice. Exiting!\n";
			exit_flag = true;
			break;
		}


	}
}