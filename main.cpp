#include <bits/stdc++.h>

using namespace std;

using ll = long long;

//mt19937 gen(chrono::system_clock::now().time_since_epoch().count());

vector<int> a, b;

const int small = 1 << 6;

vector<int> mul(vector<int>& a, vector<int>& b) {
    int len = a.size();
    vector<int> res(len + len);
    for (int i = 0; i < len; ++i) {
        for (int j = 0; j < len; ++j) {
            res[i + j] += a[i] * b[j];
        }
    }
    return res;
}

vector<int> kmul(vector<int>& a, vector<int>& b) {
    int len = a.size();
    if (len <= small) {
        return mul(a, b);
    }
    vector<int> res(len + len);
    int m = len / 2;
    vector<int> ar(a.begin(), a.begin() + m);
    vector<int> al(a.begin() + m, a.end());
    vector<int> br(b.begin(), b.begin() + m);
    vector<int> bl(b.begin() + m, b.end());
    vector<int> p1 = kmul(al, bl), p2 = kmul(ar, br), alr(m), blr(m);
    for (int i = 0; i < m; ++i) {
        alr[i] = al[i] + ar[i];
        blr[i] = bl[i] + br[i];
    }
    vector<int> p3 = kmul(alr, blr);
    for (int i = 0; i < len; ++i) {
        p3[i] -= p1[i] + p2[i];
        res[i] = p2[i];
    }
    for (int i = len; i < len + len; ++i) {
        res[i] = p1[i - len];
    }
    for (int i = m; i < len + m; ++i) {
        res[i] += p3[i - m];
    }
    return res;
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(nullptr);
    string s1, s2;
    cin >> s1 >> s2;
    int qwe = 1;
    if (s1[0] == '-') {
        qwe *= -1;
        s1.erase(s1.begin());
    }
    if (s2[0] == '-') {
        qwe *= -1;
        s2.erase(s2.begin());
    }
    int sz = 1;
    while (sz < (int)max(s1.size(), s2.size())) sz *= 2;
    if (qwe < 0) cout << "-";
    a.resize(sz);
    b.resize(sz);
    for (int st = 0, i = s1.size() - 1; i >= 0; --i, ++st) {
        a[st] = s1[i] - '0';
    }
    for (int st = 0, i = s2.size() - 1; i >= 0; --i, ++st) {
        b[st] = s2[i] - '0';
    }
    auto res = kmul(a, b);
    for (int i = 0; i < (int)res.size(); ++i) {
        res[i + 1] += res[i] / 10;
        res[i] %= 10;
    }
    while (res.size() > 1 && res.back() == 0) res.pop_back();
    for (int i = res.size() - 1; i >= 0; --i) {
        cout << res[i];
    }
    cout << '\n';
}



