//BINARY SEARCH

int arr[100];
int n;
int search;

int bs() {
	int first, last, middle;
	first = 0;
	last = n - 1;
	middle = (first+last)/2;
	while(first <= last) {
		if(arr[middle] < search)
			 first = middle + 1;
		else if (arr[middle] == search) {
			 return (middle+1);
		}
		else {
			 last = middle - 1;
		}
	middle = (first + last)/2;
	}
 return 0;
}

int main() {
	int i;
	get(n);
	for(i=0;i<n;i++) {
		get(arr[i]);
	}
	get(search);
	put(bs());
}
