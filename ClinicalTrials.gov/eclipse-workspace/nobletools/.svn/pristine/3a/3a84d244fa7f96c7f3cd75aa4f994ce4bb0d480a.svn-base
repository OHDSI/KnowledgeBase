package edu.pitt.ontology;

import java.util.Iterator;
import java.util.ListIterator;

/**
 * resource iterator that wrapps regular iterator
 * @author tseytlin
 */
public class DefaultResourceIterator implements IResourceIterator {
	protected Iterator it;
	protected int offset,limit, count;
	
	public DefaultResourceIterator(Iterator it){
		this.it = it;
	}
	
	public int getCount() {
		return count;
	}

	public int getLimit() {
		return limit;
	}

	public int getOffset() {
		return offset;
	}

	public Object next() {
		count++;
		return (it.hasNext())?it.next():null;
	}

	public void setLimit(int limit) {
		this.limit = limit;
	}

	public void setOffset(int offset) {
		this.offset = offset;
		//advance forward if offset is greater then current count
		if(offset > count){
			for(int i=count;i<offset && it.hasNext();i++,it.next());
		//if possible try to go backword
		}else if(offset < count){
			if(it instanceof ListIterator){
				ListIterator lit = (ListIterator) it;
				for(int i=count;i>=offset && lit.hasPrevious();i--,lit.previous());
			}
		}
		count = 0;
	}

	/**
	 * has next
	 */
	public boolean hasNext() {
		//TODO FIX THE MISTAKES OF THE WORLD EUGENE< YES U HAVE TO DO IT NOBODY ELSE WILL
		// Underlying it.hasNext() returns true even when it is empty, resulting in a
		//subsequent it.next call returning null
		if(limit > 0)
			return it.hasNext() && count < limit;
		return it.hasNext();
	}

	public void remove() {
		it.remove();
	}

}
