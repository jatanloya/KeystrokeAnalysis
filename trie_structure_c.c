#include <stdio.h>
#include<string.h>
#include <stdlib.h>
#include<iostream>
using namespace std;
struct node
{
    bool end_str;
    struct node *next[26];
};

void insert(struct node *head, string str)
{
    int i, j;
    for(i = 0;i < str.size(); ++i){
        if(head -> next[str[i] - 'a'] == NULL){
            struct node *n;
            n = new struct node;
            for(j = 0;j < 26; ++j){
                n -> next[j] = NULL;
            }
            n -> end_str = 0;
            head -> next[str[i] - 'a'] = n;
            head = n;
        }
        else head = head -> next[str[i] - 'a'];
    }
    head -> end_str = 1;
}

bool check(struct node *head, string str)
{
    int i;
    for(i = 0;i < str.size(); ++i){
        if(head -> next[str[i] - 'a'] == NULL) return false;
        else head = head -> next[str[i] - 'a'];
    }
    if(head -> end_str == 1) return true;
    else return false;
}

string s;
void traversal(struct node *head,string str)
{
	if(head->end_str==1)
		cout<<str<<endl;
	for(int i=0;i<26;i++)
	{
		if(head->next[i]!=NULL)
		{
			s=str+char('a'+i);
			traversal(head->next[i],s);
		}	
	}
}
void autocomplete(struct node *head,string str)
{
	int i=0;
	string s="";
	char k;
	while(i<str.size())
	{
		k=str[i];
		s+=k;
		if(head->next[k-'a']!=NULL)
			head=head->next[k-'a'];
		else
			return;
		i+=1;
	}
	traversal(head,s);
}
int main()
{
    int n, m, i;
    
    struct node *head;
    head = new struct node;
 
    
    for(i = 0;i < 26; ++i){
            head -> next[i] = NULL;
    }
    head -> end_str = 0;
 
    cin >> n;
    while(n--){
        string str;
        cin >> str;
        insert(head, str); 
    }
 
 
    cout<<"Enter half word"<<endl;
    string que;
    cin>>que;
 	autocomplete(head,que);   
    cin >> m; 
    while(m--){
        string str;
        cin >> str;
        if(check(head, str)) cout << "present\n";
        else cout << "not present\n";
       
    }
    
    return 0;
}
