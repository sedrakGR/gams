# Generated by ./generate_schemas.py. This file should not be modified by hand.
@0x98a9fc602475dd1d;

# Namespace setup
using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("gams::types");

# Capnfile Imports
using import "Wrench.capnp".Wrench;
using import "Header.capnp".Header;

# Type definition
struct WrenchStamped {
   header @0: Header;
   wrench @1: Wrench;
   
}