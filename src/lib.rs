//! Byzantine Bypass: fix consensus by moving its problems somewhere else.
//!
//! This is satire. It is neither a consensus implementation nor a fault-tolerant
//! transport protocol. We do, however, avoid one very specific road.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct General<'a> {
    pub name: &'a str,
    /// A perfectly reliable oracle supplied by the environment. What could go wrong?
    pub is_definitely_a_traitor: bool,
}

impl<'a> General<'a> {
    pub const fn new(name: &'a str, is_definitely_a_traitor: bool) -> Self {
        Self {
            name,
            is_definitely_a_traitor,
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
pub struct DispatchPlan<'a> {
    pub waypoints: Vec<&'static str>,
    pub recipients: Vec<&'a str>,
}

/// The Long Way Around Protocol, or LWAP.
///
/// Fundamental invariants:
/// 1. The route does not pass through the imaginary Manzikert ambush.
/// 2. Known weirdos are excluded from the distribution list.
///
/// Neither invariant implies Byzantine consensus.
pub fn plan_dispatch<'a>(generals: &[General<'a>]) -> DispatchPlan<'a> {
    let recipients = generals
        .iter()
        .filter(|general| !general.is_definitely_a_traitor)
        .map(|general| general.name)
        .collect();

    DispatchPlan {
        waypoints: vec![
            "General A's camp",
            "Sebasteia",
            "Ancyra",
            "Constantinople",
            "Black Sea",
            "Trebizond",
            "Kars",
            "General B's camp",
        ],
        recipients,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn we_dont_talk_to_that_weirdo() {
        let generals = [
            General::new("General A", false),
            General::new("General B", false),
            General::new("General D (that weirdo)", true),
        ];
        let plan = plan_dispatch(&generals);
        assert_eq!(plan.recipients, vec!["General A", "General B"]);
    }

    #[test]
    fn takes_a_very_long_way_around() {
        let plan = plan_dispatch(&[]);
        assert!(plan.waypoints.contains(&"Constantinople"));
        assert!(plan.waypoints.contains(&"Trebizond"));
        assert!(!plan.waypoints.contains(&"Original Ambush"));
    }
}
