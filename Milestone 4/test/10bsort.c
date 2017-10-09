// TEST CASE: BUBBLE SORT

int arr[100];
int n;

void swap(int, int);
void bubbleSort();

int main() {
	get(n);
	int i;
	for(i=0;i<n;i++) {
		get(arr[i]);
	}
	bubbleSort();
	for(i=0;i<n;i++) {
		put(arr[i]);
	}

}

void bubbleSort() {
	int t = n-1;
	int i,j;
	for(i=0; i < t; i++) {
		for(j=0; j < t - i; j++) {
			if(arr[j] > arr[j+1]) {
				swap(j,j+1);
			}
		}
	}
}

void swap(int i, int j) {
	int temp;
	temp = arr[i];
	arr[i] = arr[j];
	arr[j] = temp;
}