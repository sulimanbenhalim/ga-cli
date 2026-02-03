class GaCli < Formula
  include Language::Python::Virtualenv

  desc "Command-line interface for Google Analytics 4"
  homepage "https://github.com/sulimanbenhalim/ga-cli"
  url "https://files.pythonhosted.org/packages/8e/b1/30cb8b086c9b58920afbb5915a13108371b69bd8ec64f8ce0c9cdd217ec4/ga4_cli-0.1.1.tar.gz"
  sha256 "3849da0726068cc2c6c130d0e174385d54c06b19296c26383b05177766c5f20d"
  license "MIT"

  depends_on "python@3.11"

  def install
    venv = virtualenv_create(libexec, Formula["python@3.11"].bin/"python3.11")
    venv.pip_install "ga4-cli==0.1.1"
    bin.install_symlink libexec/"bin/ga-cli"
  end

  test do
    system bin/"ga-cli", "--version"
  end
end
