#!/usr/bin/perl

use strict;

use Web::Scraper;
use File::Fetch;
use URI;
use Data::Dumper;



my @NATIONS = qw( Albania Armenia Australia Austria Azerbaijan Belarus
Belgium Cyprus the_Czech_Republic Denmark Estonia Finland France
Georgia Germany Greece Hungary Iceland Ireland Israel Italy Latvia
Lithuania Macedonia Malta Moldova Montenegro Netherlands Norway Poland
Portugal Romania Russia San_Marino Serbia Slovenia
Spain Sweden Switzerland the_United_Kingdom );

# Note - this is fetching the HTML pages - it needs to scrape them to
# get the direct link to the svg file

my $flag = scraper {
    process "div.fullImageLink > a", 'uri' => '@href'
};


# <div .fullImageLink><a href="url"

for my $nation ( @NATIONS ) {
    my $uri = URI->new(svg_page($nation));
    warn("Scraping $uri");
    eval {
        my $results = $flag->scrape($uri);
        if( $results ) {
            my $svg = $results->{uri};
            warn("Downloading $svg");
            my $ff = File::Fetch->new(uri => $svg);
            my $where = $ff->fetch() || do {
                warn("Fetch $flag failed: " . $ff->error . "\n");
                next;
            };
        } else {
            warn("SVG link not found in $uri");
        }
    };
    if( $@ ) {
        warn("Something went wrong with $nation: $@");
    }
}


sub svg_page {
    my ( $nation ) = @_;

    return "http://en.wikipedia.org/wiki/File:Flag_of_${nation}.svg";
}
