"""
This module provides utility functions
"""

from auctions.models import Listing, Bid, Comment


def save_listing(title, description, starting_bid,
                 listing_image, category, added_by):
    """
    Save 'listing' while creating new
    """
    listing = Listing(title=title,
                      description=description,
                      listing_image=listing_image,
                      bid=starting_bid,
                      category_id=category,
                      user_id=added_by)
    listing.save()


def save_bid(list_id, user_id, bid, current_bid):
    """
    Save a bid and update corresponding 'Listing' column
    """
    if bid > current_bid:
        # Update current bid for listing in Listing model
        listing = Listing.objects.get(pk=list_id)
        listing.bid = bid
        listing.save()
        # If bid already exists in Bid model then update it
        if Bid.objects.filter(listing=list_id):
            update_bid = Bid.objects.get(listing=list_id)
            update_bid.user_id = user_id
            update_bid.bid = bid
            update_bid.save()
        # If this is the first bid, then create a new entry
        else:
            bid = Bid(listing_id=list_id, user_id=user_id, bid=bid)
            bid.save()


def add_to_watchlist(list_id, user_id):
    """
    Add a listing to user's watchlist
    """
    listing = Listing.objects.get(pk=list_id)
    listing.watchers.add(user_id)


def remove_from_watchlist(list_id, user_id):
    """
    Remove a listing from user's watchlist
    """
    listing = Listing.objects.get(pk=list_id)
    listing.watchers.remove(user_id)


def close_listing(list_id, user):
    """
    Close the listing
    """
    # Close the listing by setting 'is_active=False'
    listing = Listing.objects.get(pk=list_id)
    listing.is_active = False
    # Assign a winner for listing
    listing.winner = user
    listing.save()


def save_comment(list_id, user_id, comment):
    """
    Save listing comments
    """
    comment = Comment(user_id=user_id, listing_id=list_id, comment=comment)
    comment.save()
