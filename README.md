# LNContract
Django App to manage contract integrating Lightning Network.  

LNContract integrates the Business to Business context into LN Applications. Unlike retail transactions, Business to Business transactions require a lasting relationship between the parties. A manufacturer of subsystems supplier to a larger manufacturer buyer, for example, might have contracts to build those subsystems over several months or years and require milestone type payments along the way. 

LNContract manages this type of relationship, integrating into the LN Network.  At a high level, the app would manage the basic terms of a contract, parties obligations and payments, with payments through a LN channel via RPC.

Because the parties need an existing relationship, a channel would be better than a payment route. The channel itself could embody an aspect of the contract, as we'll see in a minute.

I am mindful that relying on a direct channel will require at least one utxo and so this won't scale, but this aspect could potentially be revised to use a federation or Taro as things develop.

Consider a manufacturer of electronic subsystems (seller) having a supply contract to a systems integrator (buyer). The supply contract requires:

    The seller to manufacture and deliver 12 subsystems.

    Delivery of first two units is 9 months from the date of contract and 2 units/month thereafter.

    Total Contract is for 150,000,000 sats.

    Milestone payments:

        materials on order: 25,000,000 sats

        stage 1 assembly: 15,000,000 sats

        stage 2 assembly: 30,000,000 sats

        subsystem testing: 60,000,000 sats

        delivery and acceptance: 20,000,000 sats

But would the seller even start work on this without anything? Maybe if he knew money was ear-marked for the contract. The channel itself could serve this purpose, acting as a quasi Letter of Credit. Buyer could give the seller some comfort by funding a channel for 30,000,000 sats at contract signing and then fund further channels (or splice in more funding) at regular intervals.

The app manages the contract. It would create funding and payment terms. It would create invoices and receive payments. It would effect all of this through an RPC connection to its LN Node and ultimately to the counterparty's node via the channel. Ideally, the counterparty would also be using the app, which the contract could require.
