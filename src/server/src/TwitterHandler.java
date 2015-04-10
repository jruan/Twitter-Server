package edu.ucsd.cse124;

import java.util.Collections;
import java.util.List;
import java.util.LinkedList;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Set;
public class TwitterHandler implements Twitter.Iface {

    protected HashMap<String, User> UserMap = new HashMap<String, User>();

    //map Tweet with their tweetID
    protected HashMap<Long, Tweet> TweetMap = new HashMap<Long, Tweet>();

    //maps user with a list of their Tweets
    protected HashMap<String, ArrayList<Tweet>> UserTweet = new HashMap<String, ArrayList<Tweet>>();

    //tweetID starts at 0
    protected long tweetID = 0;  
   

    @Override
    public void ping() {
	System.out.println("ping");
    }

    /* createUser(String handle) -> input handle is the username of the user
     * Checks to see if the user is in the database, if not, add him. Creating user = Success
     * If User is already in the database, do not add him, throw exception 
     */
    public void createUser(String handle) throws AlreadyExistsException
    {
	synchronized(UserMap){
		if(!(UserMap.containsKey(handle)))
			UserMap.put(handle, new User());
		
		else
			throw new AlreadyExistsException();
	}
    }

    /* subscribe(String handle, String theirhandle) -> input handle = user, theirhandle = user you are subscribing too
     * First, checks if handle and their handle exists. If not, throw exception. Subscription failed.
     * If it does, add the subscriber to the list of already subscribed users for that user.
     */
    public void subscribe(String handle, String theirhandle)
        throws NoSuchUserException
    {
	synchronized(UserMap){	
		//checks if the user trying to subscribe exists. If not, throw exception
		if(!(UserMap.containsKey(handle)))
			throw new NoSuchUserException();

		//Checks if the user you are trying to subscribe to exists. If not, throw exception
		if(!(UserMap.containsKey(theirhandle)))
			throw new NoSuchUserException();
	
		User u = UserMap.get(handle);
		List<String> l = u.subscribedTo;
	
		//if user not subscribed, add him to the user's subscription list
		if(!(l.contains(theirhandle)))
			l.add(theirhandle);
	}
    }
	
    @Override
    public void unsubscribe(String handle, String theirhandle)
        throws NoSuchUserException
    {
		synchronized(UserMap){
			//checks if the user trying to unsubscribe from exists. If not, throw exception
			if(!(UserMap.containsKey(handle)))
				throw new NoSuchUserException();

			//Checks if the user you are trying to unsubscribe from exists. If not, throw exception
			if(!(UserMap.containsKey(theirhandle)))
				throw new NoSuchUserException();

			User u = UserMap.get(handle);	
			List<String> subscriptionList = u.subscribedTo;
		
			//nop, if you are unsubscribing from a user you are not subscribed to, do nothing, act as nop
			if(!(subscriptionList.contains(theirhandle)))
				return;
			
			//if not remove from the list
			else
				subscriptionList.remove(theirhandle);
		}
    }

    @Override
    public void post(String handle, String tweetString)
        throws NoSuchUserException, TweetTooLongException
    {
		synchronized(UserMap){
			synchronized(TweetMap){
				synchronized(UserTweet){
					if(!(UserMap.containsKey(handle))){
						throw new NoSuchUserException();
					}
					if(tweetString.length() > 140){
						throw new TweetTooLongException();
					}		

					long posted = System.currentTimeMillis()/1000;
					int numStar = 0; 
					Tweet message = new Tweet(tweetID, handle, posted, numStar, tweetString);
					TweetMap.put(tweetID, message);

					//change the ID number
					tweetID++;

					//Add the tweet to the list of tweets by user	
					if(!UserTweet.containsKey(handle)){
						ArrayList<Tweet> temp = new ArrayList<Tweet>();
						temp.add(message);
						UserTweet.put(handle, temp);	
					}
					else{
						UserTweet.get(handle).add(message);
					}
				}
			}
		}
    }

    @Override
    public List<Tweet> readTweetsByUser(String handle, int howmany)
        throws NoSuchUserException
    {
	synchronized(UserMap){
		synchronized(UserTweet){
			ArrayList<Tweet> result = new ArrayList<Tweet>();
			if(!(UserMap.containsKey(handle)))
				throw new NoSuchUserException();
	
			if(!(UserTweet.containsKey(handle))){
				return result;
        		}	

			ArrayList<Tweet> temp = UserTweet.get(handle);
			Collections.sort(temp, new TweetComparator());
			for(int i = 0; i < howmany; i++){
				if( i < temp.size() ){
					result.add(temp.get(i));
				}
			}
			return result;
		}
	}
    }


    @Override
    public List<Tweet> readTweetsBySubscription(String handle, int howmany)
        throws NoSuchUserException
    {
	synchronized(UserMap){
		synchronized(UserTweet){
			//User has a list of subscription
			if(!(UserMap.containsKey(handle)))
				throw new NoSuchUserException();
	
			ArrayList<Tweet> result = new ArrayList<Tweet>();
	
			ArrayList<Tweet> temp = new ArrayList<Tweet>();

			User u = UserMap.get(handle);
			ArrayList<String> subscription = u.subscribedTo;
			for( String users : subscription){
				temp.addAll( readTweetsByUser(users, UserTweet.get(users).size()) );
			}
	
			Collections.sort(temp, new TweetComparator());

			for(int i = 0; i < howmany; i++){
				if(i < temp.size())
					result.add(temp.get(i));
			}
        		return result;
		}
	}
    }

    @Override
    public void star(String handle, long tweetId) throws
        NoSuchUserException, NoSuchTweetException
    {
	synchronized(UserMap){
		synchronized(TweetMap){
				
			//ensures that only valid users can rate, if not throw exception
			if(!(UserMap.containsKey(handle)))
				throw new NoSuchUserException();
			
			//ensures that only valid tweets can be rated, if not, throw exception
			if(!(TweetMap.containsKey(tweetId)))
				throw new NoSuchTweetException();

			User u = UserMap.get(handle);
			List<Long> userAlreadyRatedList = u.ratedTweetId;
		
			/*ensure that the user has never rated this tweet before. If he hasn't, 
			 *add him to the list of users that have rated the tweet. Increase the count for 
			 *number of rates for this particular Tweet by 1
			 */
			 if(!(userAlreadyRatedList.contains(tweetId))){
				userAlreadyRatedList.add(tweetId);
				Tweet t = TweetMap.get(tweetId);
				t.numStars += 1;
				TweetMap.put(tweetId, t);
			 }
		}
	}
    }
}
