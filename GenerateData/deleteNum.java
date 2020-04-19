public void deleteNum(int n){
      Node temp = head;
      while(temp!=null){
        for(int i = 0 ; i <=n-1 ;i++){
          // we traverse till previous node of 
          // the element we want to delete
          // so if we want to delete every nth element
          // temp after the for loop is at n-1th position
          temp = temp.next; 
        }
        // n-1 points to n+1 now. n is deleted.
        temp.next = temp.next.next;
        temp = temp.next;
      }
    }

public Node reverseList(){
      Node prev ;
      while(head != null){
        Node temp = head.next; // keeping of the next elemt
        head.next = prev; //reversing the pointer
        prev = head; // 
        head = temp;
      }
    return head;    
    }