#include <stdint.h>
#include <stdlib.h>

typedef struct q_item
{
uint32_t value;
struct q_item *next;
} queue_item;

typedef struct
{
queue_item *head;
} queue;


queue *queue_new(void)
{
    queue *this = malloc(sizeof(queue));
    this->head = NULL;
    return this;
}

void queue_enqueue(queue *this, uint32_t value) {
    queue_item *another = malloc(sizeof(queue_item));
    another->value = value;
    another->next = NULL;

    if (this->head == NULL)
        this->head = another;

    else {
        queue_item *current = this->head;
        while (current->next != NULL)
            current = current->next;
        
        current->next = another;
    }
}

int64_t queue_dequeue(queue *this)
{
int64_t answer;
if (this->head == NULL)
    answer = -1; // the queue is empty
else if (this->head->next == NULL) {
    answer = this->head->value;
    free(this->head);
    this->head = NULL;
}
else {
    answer = this->head->value;
    queue_item *remainder = this->head->next;
    free(this->head);
    this->head = remainder;
}
return answer;
}

queue *queue_deep_copy(queue *this) {
    queue *copy = queue_new();
    
    queue_item *current = this->head;

    while (current != NULL) {
        queue_enqueue(copy, current->value);
        current = current->next;
    }

    return copy;
}

