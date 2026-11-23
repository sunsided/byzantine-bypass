(** * The Long Way Around Protocol: a machine-checked soundness proof

    This file formalises Section IV of the README. Every lemma is fully
    verified by Coq. The theorem is also fully verified by Coq, which is
    exactly what makes it worrying.

    The model mirrors [plan_dispatch] in [src/lib.rs]. Nothing keeps the two
    in sync except good intentions, which we consider a trusted component.

    Check with: [coqc proofs/LWAP.v] *)

From Coq Require Import List Bool.
Import ListNotations.

(** ** Geography *)

Inductive place :=
  | GeneralAsCamp
  | Sebasteia
  | Ancyra
  | Constantinople
  | BlackSea
  | Trebizond
  | Kars
  | GeneralBsCamp
  | Manzikert.

Definition place_eq_dec (x y : place) : {x = y} + {x <> y}.
Proof. decide equality. Defined.

(** The route from [plan_dispatch]. Scenic. *)
Definition route : list place :=
  [ GeneralAsCamp; Sebasteia; Ancyra; Constantinople;
    BlackSea; Trebizond; Kars; GeneralBsCamp ].

(** The one and only ambush, located by assumption. *)
Definition ambush : place := Manzikert.

(** A messenger can only be intercepted somewhere he actually goes. *)
Definition intercepted_at (p : place) (r : list place) : Prop := In p r.

(** ** Lemma 1 — Ambush avoidance *)

Lemma ambush_avoidance : ~ intercepted_at ambush route.
Proof.
  unfold intercepted_at, ambush, route.
  simpl. intuition discriminate.
Qed.

(** The route does at least begin and end in the right places. *)
Lemma route_is_a_route :
  hd_error route = Some GeneralAsCamp /\ last route Manzikert = GeneralBsCamp.
Proof. split; reflexivity. Qed.

(** ** Generals *)

Record general := {
  name : nat;  (** Names are hard. Numbers are fine. *)
  (** A perfectly reliable oracle supplied by the environment. *)
  is_definitely_a_traitor : bool;
}.

Definition recipients (gs : list general) : list general :=
  filter (fun g => negb (is_definitely_a_traitor g)) gs.

(** ** Lemma 2 — The weirdo principle *)

Lemma weirdo_principle :
  forall g gs, is_definitely_a_traitor g = true -> ~ In g (recipients gs).
Proof.
  intros g gs Hweird Hin.
  unfold recipients in Hin.
  apply filter_In in Hin as [_ Hnot_weird].
  rewrite Hweird in Hnot_weird.
  discriminate.
Qed.

(** Honest generals are not accidentally ghosted. *)
Lemma honest_generals_still_get_mail :
  forall g gs, In g gs -> is_definitely_a_traitor g = false -> In g (recipients gs).
Proof.
  intros g gs Hin Hhonest.
  apply filter_In. rewrite Hhonest. auto.
Qed.

(** ** Theorem — Byzantine tolerance

    The README lists the conditions under which the protocol solves the
    Byzantine Generals Problem. We state them as hypotheses. Coq, to its
    credit, does not ask where they came from. *)

Section ByzantineTolerance.

  (** Whatever the generals were trying to agree on. Not our department. *)
  Variable byzantine_agreement : Prop.

  Hypothesis the_only_ambush_is_the_known_ambush :
    forall p r, intercepted_at p r -> p = ambush.

  Hypothesis the_excluded_general_is_the_only_traitor :
    forall gs g, In g (recipients gs) -> is_definitely_a_traitor g = false.

  Hypothesis all_other_routes_are_safe : True.

  Hypothesis all_remaining_generals_agree_on_the_exclusion : True.

  (** Load-bearing. *)
  Hypothesis message_delivery_is_otherwise_reliable :
    ~ intercepted_at ambush route -> byzantine_agreement.

  Theorem byzantine_tolerance : byzantine_agreement.
  Proof.
    (* The troublesome assumptions have been relocated from the protocol
       to the environment. *)
    apply message_delivery_is_otherwise_reliable.
    exact ambush_avoidance.
  Qed.

End ByzantineTolerance.

(** No axioms were harmed in the making of this proof. The hypotheses above
    are not axioms. They are the reader's problem. *)
Print Assumptions byzantine_tolerance.
