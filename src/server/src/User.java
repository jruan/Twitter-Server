package edu.ucsd.cse124;

import java.util.List;
import java.util.ArrayList;

public class User {
	public ArrayList<String> subscribedTo;
	public List<Long> ratedTweetId;
	
	public User(){
		subscribedTo = new ArrayList<String>();
		ratedTweetId = new ArrayList<Long>();
	}

}
