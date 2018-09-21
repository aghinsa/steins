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
        ListNode *lh,*lt,*lnp;
        lnp=ln->prev;
        lh=l.get_head();
        lt=l.get_tail();
        lt->next=ln;
        ln->prev=lt;
        if(lnp!=NULL)
        {
          lnp->next=lh;
          lh->prev=lnp;
        }
        else
        {
          begin=lh;
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

int main() {
    int n, i, op, v1, v2;
    ListNode *ln;
    cin >> n;
    List l = List();
    map<int, ListNode*> vp;
    while (n--) {
        cin >> op;
        switch (op) {
        // push back
        case 1:
            cin >> v1;
            ln = l.push_back(v1);
            assert(ln->val == v1);
            vp[v1] = ln;
            break;
        // push front
        case 2:
            cin >> v1;
            ln = l.push_front(v1);
            assert(ln->val == v1);
            vp[v1] = ln;
            break;
        // insert
        case 3:
            cin >> v1 >> v2;
            if (vp.find(v1) != vp.end()) {
                ln = l.insert(vp[v1], v2);
                assert(ln->val == v2);
                vp[v2] = ln;
            }
            break;
        // is empty?
        case 4:
            cout << l.is_empty() << endl;
            break;
        // move to front
        case 5:
            cin >> v1;
            if (vp.find(v1) != vp.end()) {
                l.move_to_front(vp[v1]);
            }
            break;
        // swap pairs
        case 6:
            l.swap_pairs();
            break;
        // reverse segment
        case 7:
            cin >> v1 >> v2;
            if (vp.find(v1) != vp.end() && vp.find(v2) != vp.end()) {
                ln = vp[v1];
                while (ln != NULL && ln != vp[v2]) {
                    ln = ln->next;
                }
                if (ln != NULL) {
                    l.reverse_segment(vp[v1], vp[v2]);
                }
            }
            break;
        // splice
        case 8:
            int num;
            cin >> v1 >> num;
            if (vp.find(v1) != vp.end()) {
                List l1;
                for (i=0; i<num; i++) {
                    cin >> v2;
                    ln = l1.push_back(v2);
                    assert(ln->val == v2);
                    vp[v2] = ln;
                }
                l.splice(vp[v1], l1);
            }
            break;
        // print
        case 9:
            l.print();
            break;
        }
    }
}
