//QUICK SORT

int arr[100];
int n;

void swap(int, int);
int partition (int, int);
void quickSort(int, int);

int partition (int low, int high){
	int pivot = arr[high];
	int i = (low - 1);
	int t;
	for(int j = low; j <= high- 1; j++){
		if (arr[j] <= pivot){
			i++;
			swap(i,j);
		}
	}
	swap(i+1,high);
	return (i + 1);
}
void quickSort(int low, int high){
	int pi;
	if(low < high) {
		pi = partition(low, high);
		quickSort(low, pi - 1);
		quickSort(pi + 1, high);
	}
}
 
void swap(int i, int j) {
	int temp;
	temp = arr[i];
	arr[i] = arr[j];
	arr[j] = temp;
}

int main() {
	get(n);
	int i;
	for(i=0;i<n;i++) {
		get(arr[i]);
	}
	quickSort(0, n-1);
	for(i=0;i<n;i++) {
		put(arr[i]);
	}
}


 
