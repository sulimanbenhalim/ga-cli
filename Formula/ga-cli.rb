class GaCli < Formula
  include Language::Python::Virtualenv

  desc "Command-line interface for Google Analytics 4"
  homepage "https://github.com/sulimanbenhalim/ga-cli"
  url "https://files.pythonhosted.org/packages/dd/55/fe60133f220ff31795e00046e7a8cd868334af17ec0bc37b0dc0083e7536/ga4_cli-0.1.0.tar.gz"
  sha256 "a7a9d60a92487050ed405776f688c6841cd184c5e5af0d95459b91c5125d8495"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"ga-cli", "--version"
    assert_match "0.1.0", shell_output("#{bin}/ga-cli --version")
  end
end
