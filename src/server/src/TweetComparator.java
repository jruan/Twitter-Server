package edu.ucsd.cse124;

import java.util.Comparator;

public class TweetComparator implements Comparator{

	@Override
	public int compare(Object o1, Object o2){
		Tweet t1 = (Tweet)o1;
		Tweet t2 = (Tweet)o2;
		return (int)t2.tweetId - (int)t1.tweetId;

	}

}
