//MATRIX MULTIPLICATIONs

int main(){
		int a1[73][73];
		int a2[73][73];
		int a73[73][73];

		int i, j, k, sum = 0;
		int n;
		get(n);
		for(i=0;i<n;i++) {
			for(j=0;j<n;j++) {
				get(a1[i][j]);
			}
		}
		for(i=0;i<n;i++) {
			for(j=0;j<n;j++) {
				get(a2[i][j]);
			}
		}
		for (i = 0; i < n; i++) {
			for (j = 0; j < n; j++) {
				for (k = 0; k < n; k++) {	
					sum = sum + a1[i][k]*a2[k][j];
				}
 
				a73[i][j] = sum;
				sum = 0;
			}
		}

		for(i=0;i<n;i++) {
			for(j=0;j<n;j++) {
				put(a73[i][j]);
			}
		}
}