#!/usr/bin/perl

use strict;
use Data::Dumper;

my @DEPTH = ( 10, 20, 30, 40 );

my @PATH1 = (
    [ 0, 0, 10 ],
    [ 5, 2, 20 ],
    [ 10, 5, 30 ],
    [ 15, 7, 40 ],
    [ 10, 5, 30 ],
    [ 5, 2, 20 ]
    );

my @PATH2 = (
    [ 0, 0, 40 ],
    [ 0, 0, 30 ],
    [ 0, 0, 20 ],
    [ 0, 0, 10 ],
    [ 10, 5, 20 ],
    [ 20, 10, 30 ],
    [ 30, 15, 40 ],
    [ 30, 10, 40 ],
    [ 30, 5, 40 ],
    [ 30, 0, 40 ],
    [ 20, 0, 30 ],
    [ 10, 0, 20 ],
    [ 0, 0, 10 ],
    [ 0, 5, 20 ],
    [ 0, 10, 30 ],
    [ 0, 15, 40 ],
    [ 0, 10, 40 ],
    [ 0, 5, 40 ]
    );

my @PATH3 = (
    [ 0, 0, 20 ],
    [ 0, 0, 18 ],
    [ 0, 0, 16 ],
    [ 0, 0, 14 ],
    [ 0, 0, 12 ],
    [ 0, 0, 10 ],
    [ 0, 0, 10 ],
    [ 2, 1, 12 ],
    [ 4, 2, 14 ],
    [ 6, 3, 16 ],
    [ 8, 4, 18 ],
    [ 10, 5, 20 ],
    [ 10, 4, 20 ],
    [ 10, 3, 20 ],
    [ 10, 2, 20 ],
    [ 10, 1, 20 ],
    [ 10, 0, 20 ],
    [ 8, 0, 18 ],
    [ 6, 0, 16 ],
    [ 4, 0, 14 ],
    [ 2, 0, 12 ],
    [ 0, 0, 10 ],
    [ 0, 0, 10 ],
    [ 0, 1, 12 ],
    [ 0, 2, 14 ],
    [ 0, 3, 16 ],
    [ 0, 4, 18 ],
    [ 0, 5, 20 ],
    [ 0, 4, 20 ],
    [ 0, 3, 20 ],
    [ 0, 2, 20 ],
    [ 0, 1, 20 ]
    );
    

my @PATH = @PATH3;


my $grids = {};

for my $file ( @ARGV ) {
    if( $file =~ /Flag_of_([^.]+)\/(\d+)\.ppm/ ) {
        my $country = lc($1);
        my $depth = $2;
        $grids->{$country}{$depth} = ppm_to_grid($file);
        warn "$country $depth\n";
    }
}

print "FRAMES = {}\n\n";

for my $country ( sort keys %$grids ) {
    my $frames = apply_path($grids->{$country});
    python_out($country, $frames);
}




sub ppm_to_grid {
    my ( $file ) = @_;

    open FH, "<", $file || die("Couldn't open $file $!");

    my $format = <FH>;
    my $geometry = <FH>;
    my $depth = <FH>;

    chomp $geometry;
    my ( $width, $height ) = split(/\s/, $geometry); 
    
    my @values = ();
    
    while ( <FH> ) {
        chomp;
        push @values, split;
    }

    my @rows = ();

    my $row = [];

    while ( @values ) {
        my $r = shift @values;
        my $g = shift @values;
        my $b = shift @values;
        if( ! defined $b || ! defined $g ) {
            warn("Wrong number of values in $file\n");
        }
        push @$row, [ $r, $g, $b ];
        if( scalar @$row == $width ) {
            push @rows, $row;
            $row = [];
        }
    }
    warn "$width x $height\n";
    
    return \@rows;
}


sub apply_path {
    my ( $grids ) = @_;

    my $frames = [];

    for my $point ( @PATH ) {
        my ( $x0, $y0, $z ) = @$point;
        my $frame = [];
        if( !defined $grids->{$z} ) {
            die("No ppm $z");
        }
        for my $y ( 0..4 ) {
            for my $x ( 0..9 ) {
                if( defined $grids->{$z}[$y0 + $y][$x0 + $x] ) {
                    $frame->[$y][$x] = $grids->{$z}[$y0 + $y][$x0 + $x];
                } else {
                    die("Frame out of bounds at $x0 $x $y0 $y $z");
                }
            }
        }
        push @$frames, $frame;
    }
    return $frames;
}


sub python_out {
    my ( $country, $frames ) = @_;

#    print Dumper ( { country => $country, frames => $frames });

   
    print "FRAMES['$country'] = []\n";

    for my $f ( @$frames ) {
        print "FRAMES['$country'].append(";
        print frame_to_array($f);
        print ")\n\n";
    }
}


sub frame_to_array {
    my ( $frame ) = @_;
    my $lights = frame_to_holiday($frame);
    my $array = "[ ";
    $array .= join(', ', map { '(' . join(', ', @$_) . ')' } @$lights);
    $array .= " ]";
    return $array;
}



sub frame_to_holiday {
    my ( $frame ) = @_;

    my @new = @{$frame->[0]};
    push @new, reverse @{$frame->[1]};
    push @new, @{$frame->[2]};
    push @new, reverse @{$frame->[3]};
    push @new, @{$frame->[4]};

    my @r = reverse @new;
    
    return \@r;
}
 

