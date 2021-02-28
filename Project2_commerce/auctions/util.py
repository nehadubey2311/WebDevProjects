from auctions.models import Listings

def save_listing(title, description, starting_bid, listing_image, category, added_by):
    listing = Listings(title=title, description=description, listing_image=listing_image, starting_bid=starting_bid, category=category, list_id=added_by)
    listing.save()