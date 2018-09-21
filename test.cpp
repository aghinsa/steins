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
       else
       {
         ListNode *lnp;
         lnp=ln->prev;
         begin->prev=ln;
         lnp->next=ln->next;
         ln->next->prev=lnp;
         ln->next=begin;
         begin=ln;
         ln->prev=NULL;

       }
      }

      void swap_pairs()
      {
        // 6: swap pairs
      if(begin==end)
        return;
      ListNode *a,*b;
      a=begin;
      b=begin->next;
      while(true)
      {
        swap(a,b);
        a=a->next;
        if(a==NULL)
          break;
        b=a->next;
        if(b==NULL)
          break;
      }
    }

      void reverse_segment(ListNode *ln1, ListNode *ln2)
      {
        ListNode *ln1n,*ln2p;
        ListNode* a[3];

        while(ln1!=ln2)
        {
          a[1]=ln1;
          a[2]=ln2;
          ln1n=ln1->next;
          ln2p=ln2->prev;
          swap(ln1,ln2);
          ln1=ln1n;
          ln2=ln2p;
          if(ln1==a[2])
            break;
        }
      }

      void swap(ListNode *a,ListNode *b)
      {
        if(a->next!=b)
        {
          ListNode *ap,*bn,*an;
          an=a->next;
          bn=b->next;
          ap=a->prev;
          a->next=b->next;
          if(bn!=NULL)
            bn->prev=a;
          else
          {
            end=a;
            a->next=NULL;
          }
          b->prev->next=a;
          a->prev=b->prev;
          if(ap!=NULL)
            ap->next=b;
          else
          {
            begin=b;
            b->prev=NULL;
          }
          b->prev=ap;
          an->prev=b;
          b->next=an;
        }
        else
        {
          ListNode *ap,*bn;
          bn=b->next;
          ap=a->prev;

          a->next=b->next;
          if(bn!=NULL)
            b->next->prev=a;
          else
            {
              end=a;
              a->next=NULL;
            }
          a->prev=b;
          b->next=a;
          if(ap!=NULL)
          {
            ap->next=b;
            b->prev=ap;
          }
          else
          {
            begin=b;
            b->prev=NULL;
          }
        }
      }

      void splice(ListNode *ln, List l)
      {
        if(ln==begin)
        {
          begin=l.get_head();
          l.get_tail()->next=ln;
          ln->prev=l.get_tail();
        }
        else
        {
          l.get_tail()->next=ln;
          ln->prev->next=l.get_head();
          l.get_head()->prev=ln->prev;
          ln->prev=l.get_tail();
        }
      }

      ListNode* get_head(){return begin;}
      ListNode* get_tail(){return end;}

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
    List l,q;
    ListNode *a,*b;
    a=l.push_back(1);
    b=l.push_back(2);
    l.push_back(3);
    l.push_back(4);
    //l.push_back(5);



    for(int i=10;i<=12;i++)
      q.push_back(i);

    l.print();
    cout<<endl;
    q.print();
    cout<<endl;

    // l.reverse_segment(a,b);
    // l.print();
    // cout<<endl;

    //l.splice(a,q);
    l.move_to_front(b);
    l.print();
    cout<<endl;

    // l.swap_pairs();
    // l.print();
    // cout<<endl;


    return 0;
  }
