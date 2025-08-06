


# LOGIC
# First off, you should go chunk by chunk, adding them until tokens > 400
# Once tokens is bigger than 400, the idea is to take the index of the first semantic chunk in this unified chunk (let's say it's N)
# And integrate at the beggining N-1. If the token size of N-1 is less than 80, then integrate N-2 at the beginning too (before N-1)
# if now the tokens_(N-1) + tokens_(N-2) > 80 then stop like that and continue to form the next unified chunk from M+1 (M is the index 
# of the last semantic chunk in the now formed unified chunk.
# The idea is to repeat this process each time until you have done the whole code.
# semantic_chunks: [{"content": str, "tokens": int}, ...]

def my_chunk_overlapper(semantic_chunks):

    # go chunk by chunk and add them, until the sum of the tokens is over 400
    # how do you know when to stop? you need to stop once you have reached the last chunk in the index
    # so you can have some kind of curr_index, that will point to the chunk you are in right now
    # then you can have some sort of first_index_new_chunk which will point to the index of the first chunk in the current chunk we're in
    
    curr_index = 0
    new_chunks = []
    while curr_index < len(semantic_chunks):
        first_index_new_chunk = curr_index
        new_chunk = {"content": "", "tokens": 0}

        while new_chunk["tokens"] < 400:
            new_chunk["content"] += semantic_chunks[curr_index]["content"]
            new_chunk["tokens"] += semantic_chunks[curr_index]["tokens"]
            curr_index += 1
            # once the token count of the new_chunk reaches 400 this will stop
            
        # once reached this point, technically the "unified chunk" is already created
        # this is the point in which i am supposed to add the overlap
        
        reverse_index = first_index_new_chunk - 1
        overlap = ""
        overlap_tokens = 0
        while reverse_index > 0 and overlap_tokens < 80:
            overlap = semantic_chunks[reverse_index]["content"] + overlap
            overlap_tokens += semantic_chunks[reverse_index]["tokens"]

        new_chunk["content"] = overlap + new_chunk["content"]
        new_chunks.append(new_chunk)
