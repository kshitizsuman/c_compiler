int arr[3];
int n;

int partition (int low, int high){
    int pivot = arr[high];
    int i = (low - 1);
    int t;
    for(int j = low; j <= high- 1; j++){
        if (arr[j] <= pivot){
            i++;
            t = arr[i];
		    arr[i] = arr[j];
		    arr[j] = t;
        }
    }
    t = arr[i + 1];
	arr[i + 1] = arr[high];
	arr[high] = t;
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
 
void printArray()
{
    int i;
    for(i=0; i<n; i++)
        put(arr[i]);
}
 
int main()
{
	n = 3;
    arr[0] = 10;
    arr[1] = 7;
    arr[2] = 8;
    // arr[3] = 9;
    // arr[4] = 1;
    // arr[5] = 5;
    
    quickSort(0, n-1);
    
    printArray();
}


