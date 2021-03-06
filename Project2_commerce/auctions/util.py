from auctions.models import Listing, Bid, Comment

def save_listing(title, description, starting_bid, listing_image, category, added_by):
    """[summary]
    Save 'listing' while creating new
    """
    listing = Listing(title=title, description=description, listing_image=listing_image,
                      starting_bid=starting_bid, category_id=category, user_id=added_by)
    listing.save()


def save_bid(list_id, user_id, bid, start_bid):
    """
    Save a bid and update corresponding 'Listing' column
    """
    if bid > start_bid:
        # Update current bid for listing
        listing = Listing.objects.get(pk=list_id)
        listing.starting_bid = bid
        listing.save()
        # Save bid
        if Bid.objects.filter(listing=list_id):
            update_bid = Bid.objects.get(listing=list_id)
            update_bid.user_id = user_id
            update_bid.bid = bid
            update_bid.save()
        else:
            bid = Bid(listing_id=list_id, user_id=user_id, bid=bid)
            bid.save()

def add_to_watchlist(list_id, user_id):
    """[summary]
    Add a listing to user's watchlist
    """
    listing = Listing.objects.get(pk=list_id)
    listing.watchers.add(user_id)

def remove_from_watchlist(list_id, user_id):
    """[summary]
    Remove a listing from user's watchlist
    """
    listing = Listing.objects.get(pk=list_id)
    listing.watchers.remove(user_id)

def close_listing(list_id, user):
    # Close the listing by setting 'is_active=False'
    listing = Listing.objects.get(pk=list_id)
    listing.is_active = False
    # Assign a winner for listing
    listing.winner = user
    listing.save()

def save_comment(list_id, user_id, comment):
    comment = Comment(user_id=user_id, listing_id=list_id, comment=comment)
    comment.save()
