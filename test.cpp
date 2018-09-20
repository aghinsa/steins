#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode *next, *prev;

    ListNode() {
        next = prev = NULL;
    }
};

class List {
    ListNode *begin, *end;

    public:
      List()
      {
          begin = end = NULL;
      }

      ListNode* push_back(int val)
      {
        // 1: push to end
        ListNode *currNode=new ListNode;
        if (begin==NULL)
        {
          currNode->val=val;
          currNode->next=NULL;
          currNode->prev=NULL;
          begin=currNode;
          end=currNode;
        }
        else
        {
          currNode->prev=end;
          end->next=currNode;
          end=currNode;
          currNode->next=NULL;

          currNode->val=val;
        }
        return currNode;
      }

      ListNode* push_front(int val)
      {
        // 2: push to start
        ListNode *currNode=new ListNode;
        if (begin==NULL)
        {
          currNode->val=val;
          currNode->next=NULL;
          currNode->prev=NULL;
          begin=currNode;
          end=currNode;
        }
        else
        {
          currNode->val=val;
          currNode->next=begin;
          begin->prev=currNode;
          begin=currNode;
          currNode->prev=NULL;

        }
        return currNode;
      }

      ListNode* insert(ListNode *ln, int val)
      {
        // 3: insert
        ListNode *currNode=new ListNode;
        if (ln==begin)
          return push_front(val);
        currNode->next=ln;
        ln->prev->next=currNode;
        currNode->prev=ln->prev;
        ln->prev=currNode;
        currNode->val=val;
        return currNode;
      }

      bool is_empty()
      {
        // 4: check if empty
        if (begin==end)
          return true;
        return false;
      }

      void move_to_front(ListNode *ln)
      {
        // 5: move to front
        if(ln==begin)
          return;
        if(ln==end)
        {
          end=ln->prev;
          end->next=NULL;
          ln->prev=NULL;
          ln->next=begin;
          begin->prev=ln;
          begin=ln;
        }
      }

      void swap_pairs()
      {
        // 6: swap pairs
        if(begin==end)
          return;
        ListNode *idx,*idxPrev;
        ListNode *temp=new ListNode;
        idx=begin;
        do
        {
          if(idx->prev==NULL)
          {
              idx->next->prev=NULL;
              begin=idx->next;
              idx->next=idx->next->next;
              if(  begin->next!=NULL)
              {
                begin->next->prev=idx;
                begin->next=idx;
                idx->prev=begin;

                idxPrev=idx;
                idx=idx->next;
                continue;
              }
              else
              {
                end=idx;
                end->next=NULL;
                idxPrev=idx;
                begin->next=idx;
                idx->prev=begin;
                //idx=idx->next;
                break;
              }

          }

          idx->prev->next=idx->next;
          idx->next->prev=idx->prev;
          idx->prev=idx->next;
          idx->next=idx->next->next;
          idx->prev->next=idx;
          idx->next->prev=idx;
          //need to update idx
          idxPrev=idx;
          idx=idx->next;
        }while(idxPrev->next->next!=NULL);

        if(idxPrev->next==NULL)
          end=idxPrev->next;
        else
          end=idxPrev->next->next;

      }

      void print()
      {
        // 9: print all elements
        ListNode *cp;
        cp=begin;
        while(cp!=NULL)
        {
          cout<<cp->val<<' ';
          cp=cp->next;
        }
      }
  };

  int main()
  {
    List l;
    for(int i=1;i<=2;i++)
      l.push_front(i);
    l.print();
    l.swap_pairs();
    cout<<endl;
    l.print();

    return 0;
  }
