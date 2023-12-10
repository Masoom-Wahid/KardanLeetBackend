#include <iostream>

using namespace std;
int main(){
  nt tst;
  cin>>tst;
  for(int i=0;i<tst;i++){
    int fac;
    cin >>fac;
    long long res = 1;
    for (int j = 1;j <= fac;j++){
      res = res * j;
    }
    cout<<res<<endl;
  }

}
