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
          //this is chane
          if(idx->next==NULL)
          {
            idxPrev=idx;
            idx=idx->next;
            break;
          }
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

      void reverse_segment(ListNode *ln1, ListNode *ln2)
      {
        // 7: reverse list from nodes ln1 to ln2
        // if(l1==begin)

        //   begin=l2;
        ListNode *idxe,*idxb,*idxiprev,*idxinext;
        idxinext=ln2->next;
        idxiprev=ln1->prev;
        idxe=ln2;
        idxb=ln1;
        while(true)
        {
          idxe->next=ln1;
          if(idxinext!=NULL)
            idxinext->prev=idxe->prev;
          else
            end=idxe->prev;
          idxe->prev->next=idxinext;
          idxe->prev=idxb->prev;
          if(idxiprev!=NULL)
            idxb->prev->next=idxe;
          else
            begin=idxe;
          idxb->prev=idxe;
          //update
          if(idxinext!=NULL)
            idxe=idxinext->prev;
          else
            idxe=end;
          if(idxiprev!=NULL)
            idxb=idxiprev->next;
          else
            idxb=begin;

          if(idxe==ln1)
            break;

        }
      }

      void splice(ListNode *ln, List l)
      {
        // 8: splice
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
    ListNode *a,*b;
    l.push_back(1);
    a=l.push_back(2);
    l.push_back(3);
    l.push_back(4);
    b=l.push_back(5);
    l.push_back(6)


    l.print();
    //l.swap_pairs();
    l.reverse_segment(a,b);
    cout<<endl;
    l.print();

    return 0;
  }
